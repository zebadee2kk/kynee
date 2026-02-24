# Branching & AI Collaboration Guidelines

## Purpose

This document establishes rules for multiple contributors (human and AI agents) to work on KYNEĒ simultaneously without conflicts. All contributors MUST follow these guidelines.

---

## Branching Model

### Protected Branches

**`main`**
- Always releasable, production-quality code
- Direct pushes: **DISABLED**
- Changes: Only via Pull Requests (PRs)
- Required checks: Tests pass, security scan pass, review approval
- Auto-merge: Disabled (manual merge after approval)

**`release/x.y`** (e.g., `release/0.9`)
- Created from `main` for each release
- Only receives bug fixes (cherry-picked from `main`)
- Changes merged back to `main` via PR
- Example: `release/0.9` → tag `v0.9.0` → hotfix → `v0.9.1` → PR to `main`

### Short-Lived Topic Branches

All work happens in short-lived branches with conventional naming:

**Naming Convention**:
- `feat/<area>-<short-description>` — New features
- `fix/<area>-<short-description>` — Bug fixes
- `docs/<area>-<short-description>` — Documentation updates
- `chore/<area>-<short-description>` — Maintenance (deps, CI, etc.)
- `test/<area>-<short-description>` — Test additions/fixes

**Area Keywords**:
- `agent` — Agent codebase (`agent/`)
- `console-backend` — Console backend (`console/backend/`)
- `console-frontend` — Console frontend (`console/frontend/`)
- `infra` — Infrastructure (Docker, Terraform, etc.)
- `docs` — Documentation
- `hardware` — Hardware specs, BOM, compatibility

**Examples**:
- `feat/agent-collectors-network-v0`
- `feat/console-backend-auth-jwt`
- `feat/console-frontend-engagement-wizard`
- `fix/agent-wireguard-reconnect`
- `docs/legal-roe-template-polish`
- `chore/ci-security-scan-workflow`

---

## AI Agent Collaboration Rules

### Rule 1: Single-Area Ownership

Each branch must focus on **ONE** logical area:

✅ **Good**:
- `feat/agent-collectors-network` touches only `agent/aetherpi_agent/collectors/network.py`
- `feat/console-backend-api-devices` touches only `console/backend/app/api/devices.py`

❌ **Bad**:
- `feat/multiple-changes` touches `agent/`, `console/backend/`, and `docs/` in unrelated ways

**Rationale**: Reduces merge conflicts, simplifies reviews, enables parallel work.

### Rule 2: No Shared Branches

A branch is owned by **ONE** contributor (human or AI) at a time:

- Ownership declared in PR description: `Owner: AI-Agent-Alpha` or `Owner: @username`
- No concurrent edits to the same branch
- If collaboration needed, coordinate via PR comments or create a new branch

### Rule 3: Short-Lived Branches

**Target lifetime**: 1–2 days maximum

- Open PR as soon as branch is ready
- Address review feedback promptly
- Merge or close quickly to reduce divergence from `main`

**For AI agents**: If a task will take >2 days, break it into smaller incremental PRs.

### Rule 4: Serial Editing Per Path

For **structural changes** to critical paths, only **ONE** open PR at a time:

**Critical Paths**:
- `agent/aetherpi_agent/` (core agent logic)
- `console/backend/app/` (core API)
- `console/frontend/src/` (core UI)
- `schemas/*.schema.json` (data contracts)

**Example**:
- AI-Agent-Alpha opens `feat/agent-scheduler-v0` (modifies `agent/aetherpi_agent/scheduler.py`)
- AI-Agent-Beta must wait until Alpha's PR merges before opening `feat/agent-collectors-wireless`
- Exception: If Beta's work touches a completely different file (e.g., `collectors/bluetooth.py`), it can proceed in parallel

**Non-critical paths** (docs, hardware specs, examples) can have multiple concurrent PRs.

### Rule 5: Rebase Before Merge

Before submitting a PR or after `main` updates significantly:

```bash
git fetch origin
git checkout feat/your-branch
git rebase origin/main
# Resolve conflicts if any
git push --force-with-lease
```

**Why**: Keeps branch history linear, ensures tests run against latest code.

**AI agents**: Must rebase if PR conflicts with `main` or if requested by maintainers.

### Rule 6: Conventional Commits

All commits MUST follow [Conventional Commits](https://www.conventionalcommits.org/):

**Format**:
```
<type>(<scope>): <short description>

<optional body>

<optional footer>
```

**Types**:
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation only
- `style` — Formatting, no code change
- `refactor` — Code restructuring, no behavior change
- `test` — Adding/fixing tests
- `chore` — Maintenance (deps, CI, build)

**Examples**:
```
feat(agent): add network collector with nmap integration

Implements NetworkCollector class that wraps nmap and outputs
JSON per findings.schema.json.

Closes #12

fix(console): handle CSRF token expiration gracefully

docs(legal): refine RoE template language for GDPR compliance

chore(ci): add security scanning with Bandit and Semgrep
```

**AI agents**: MUST use conventional commits for all PR commits.

### Rule 7: Required Checks for AI PRs

Before submitting, AI agents must verify:

- [ ] **Linting passes**: `ruff check` (Python), `eslint` (JS/TS)
- [ ] **Formatting applied**: `black` (Python), `prettier` (JS/TS)
- [ ] **Tests pass**: `pytest` (agent/console backend), `npm test` (frontend)
- [ ] **No TODOs or commented code**: Remove or file follow-up issues
- [ ] **Documentation updated**: If behavior changes, update relevant `.md` files
- [ ] **Schema compliance**: If touching data models, validate against `schemas/*.schema.json`

### Rule 8: Conflict Avoidance for AI Agents

AI agents MUST:

✅ **Do**:
- Only modify files under assigned area
- Create new files when extending functionality
- Add tests for new code
- Update documentation inline with code changes

❌ **Don't**:
- Bulk reformat entire repo (creates massive diffs)
- Rename/move shared files without coordination
- Change whitespace in unrelated files
- Modify version numbers (see Rule 9)
- Touch files outside assigned scope

### Rule 9: Versioning Discipline

**Only maintainers** bump version numbers and create tags.

AI agents MUST NOT:
- Change version in `pyproject.toml`, `package.json`, `__init__.py`
- Create git tags
- Modify `CHANGELOG.md` (auto-generated)

**Maintainers will**:
- Bump versions after PRs merge
- Tag releases following SemVer
- Generate changelogs from conventional commits

---

## Version Control & Releases

### Semantic Versioning (SemVer)

**Format**: `MAJOR.MINOR.PATCH`

- `MAJOR`: Breaking changes (e.g., 0.x → 1.0, 1.x → 2.0)
- `MINOR`: New features, backward-compatible (e.g., 1.1 → 1.2)
- `PATCH`: Bug fixes, backward-compatible (e.g., 1.2.0 → 1.2.1)

**Pre-1.0 Releases**:
- `0.y.z` for beta/alpha releases
- `0.1.0` — Week 1 milestone
- `0.5.0` — Week 5 milestone (console v0)
- `0.9.0` — Week 8 milestone (beta release)
- `1.0.0` — First stable release (post-beta hardening)

### Git Tags

Releases are tagged as `vX.Y.Z`:

```bash
git tag -a v0.9.0 -m "Beta release: Week 8 milestone"
git push origin v0.9.0
```

**Automated via CI**: `.github/workflows/release.yml` creates GitHub Releases with artifacts.

### Release Branches

For long-term support:

1. Cut release branch: `git checkout -b release/0.9 main`
2. Push: `git push origin release/0.9`
3. Tag: `git tag v0.9.0`
4. Hotfixes: Cherry-pick to `release/0.9`, tag `v0.9.1`, merge back to `main`

---

## Pull Request (PR) Workflow

### Opening a PR

1. **Push branch**:
   ```bash
   git push origin feat/your-branch
   ```

2. **Open PR on GitHub**: Use the PR template (auto-populated)

3. **Fill required fields**:
   - **Scope**: (agent | console-backend | console-frontend | docs | infra | hardware)
   - **Owner**: (AI or human identifier)
   - **Description**: What changed and why
   - **Tests**: Commands run and results
   - **Risk**: Low / Medium / High
   - **Overlap**: Files/areas that may conflict with other branches

4. **Request review**: Tag `@maintainers` or specific reviewers

### PR Template Expectations

Each PR MUST include (see `.github/pull_request_template.md`):

```markdown
## Scope
<!-- Check one -->
- [ ] Agent
- [ ] Console Backend
- [ ] Console Frontend
- [ ] Docs
- [ ] Infrastructure
- [ ] Hardware

## Owner
<!-- AI agent name or human GitHub username -->
Owner: AI-Agent-Alpha

## Description
<!-- What changed and why -->
Implements network collector for agent using nmap wrapper.

## Tests
<!-- Commands run and results -->
```bash
pytest agent/tests/test_network_collector.py -v
# All tests passed (5/5)
```

## Risk
<!-- Low / Medium / High -->
Low — New feature, no changes to existing code

## Overlap
<!-- Files/areas that may conflict -->
None — Creates new file `agent/aetherpi_agent/collectors/network.py`

## Checklist
- [x] Tests pass
- [x] Linting/formatting applied
- [x] Documentation updated
- [x] Conventional commits used
- [x] No version number changes
```

### Review Process

1. **Automated checks**: CI runs tests, linting, security scans
2. **Human review**: Maintainer reviews code, docs, tests
3. **Feedback**: Reviewer requests changes via PR comments
4. **Iteration**: Contributor addresses feedback, pushes new commits
5. **Approval**: Reviewer approves PR
6. **Merge**: Maintainer merges (squash or rebase merge)

**AI agents**: Must address review feedback within 24 hours or PR may be closed.

---

## Conflict Resolution

### If PR Conflicts with `main`

1. **Fetch latest**:
   ```bash
   git fetch origin
   git checkout feat/your-branch
   ```

2. **Rebase**:
   ```bash
   git rebase origin/main
   ```

3. **Resolve conflicts**:
   - Edit conflicted files
   - `git add <resolved-files>`
   - `git rebase --continue`

4. **Re-run tests**:
   ```bash
   pytest  # or npm test
   ```

5. **Force-push**:
   ```bash
   git push --force-with-lease
   ```

**AI agents**: If unable to resolve conflicts automatically, flag for human review.

### If Two PRs Modify Same File

**Scenario**: AI-Agent-Alpha and AI-Agent-Beta both modify `agent/aetherpi_agent/config.py`

**Resolution**:
1. First PR to merge wins
2. Second PR must rebase onto latest `main` (includes first PR's changes)
3. Second contributor resolves conflicts manually
4. Maintainers may request second PR split into smaller, non-conflicting changes

**Prevention**: Follow Rule 4 (serial editing for critical paths)

---

## AI Agent Handover Sequence

To minimize conflicts, work is handed to AI agents in this order:

### Phase 1: Foundations (Week 1-2)
1. **Architecture AI**: ADRs, schemas, design docs (`docs/architecture/`)
2. **Platform AI**: Kali build scripts, hardening docs (`scripts/`, `docs/build/`)

### Phase 2: Agent Core (Week 3-4)
3. **Agent Features AI**: Collectors, parsers, audit logging (`agent/aetherpi_agent/`)
4. **Transport AI**: WireGuard, enrollment, protocol (`agent/aetherpi_agent/transport/`)

### Phase 3: Console (Week 5)
5. **Console Backend AI**: FastAPI, DB models, auth (`console/backend/`)
6. **Console Frontend AI**: React UI, engagement wizard (`console/frontend/`)

### Phase 4: Intelligence (Week 6)
7. **AI Assistant AI**: Prompt engineering, LLM integration (`console/backend/app/ai/`)

### Phase 5: Integration (Week 7-8)
8. **Integrations AI**: Flipper, packaging, CI/CD (`agent/collectors/flipper.py`, `.github/workflows/`)

**Key**: Each agent works in its designated area during its phase. No overlap between phases.

---

## Monitoring & Enforcement

### Branch Protection Rules (GitHub)

Configured on `main`:
- Require pull request reviews (1 approval minimum)
- Require status checks to pass:
  - `test-agent` (pytest)
  - `test-console-backend` (pytest)
  - `test-console-frontend` (npm test)
  - `security-scan` (Bandit, Semgrep)
  - `lint` (ruff, eslint)
- Require branches to be up-to-date before merge
- Restrict pushes (no direct commits)
- Require linear history (rebase or squash merge)

### Metrics

Maintainers track:
- Average PR merge time (target: <48 hours)
- Conflict rate (target: <10% of PRs)
- Test coverage (target: >80% for critical modules)
- Open PR count (target: <5 at any time)

---

## FAQs

**Q: Can I work on multiple features simultaneously?**
A: Yes, but create separate branches for each. Don't mix unrelated changes in one PR.

**Q: What if I need to change a file in another agent's area?**
A: Coordinate via GitHub Discussions or open a small, focused PR for just that change. Tag the area owner for review.

**Q: Can I force-push to my branch?**
A: Yes, use `git push --force-with-lease` (safer than `--force`). Never force-push to `main` or `release/*`.

**Q: What if CI checks fail?**
A: Fix the issues locally, commit fixes, and push. CI will re-run automatically.

**Q: How do I update my PR after review feedback?**
A: Make changes, commit with a descriptive message (e.g., `fix: address review feedback on error handling`), and push. No need to open a new PR.

**Q: What if my PR is stale (>7 days old)?**
A: Rebase onto latest `main`, address any conflicts, and notify maintainers. Stale PRs may be closed after 14 days.

---

## Summary: AI Agent Checklist

Before opening a PR, verify:

- [ ] Branch name follows convention (`feat/agent-*`, `fix/console-*`, etc.)
- [ ] Commits use conventional format (`feat(agent): ...`)
- [ ] Only modified files in assigned area
- [ ] Tests pass locally
- [ ] Linting/formatting applied
- [ ] Documentation updated (if needed)
- [ ] No version number changes
- [ ] Rebased onto latest `main`
- [ ] PR template filled out completely
- [ ] No conflicts with other open PRs (checked GitHub PR list)

---

**Last Updated**: February 24, 2026  
**Maintainer**: @zebadee2kk  
**Enforcement**: Automated via GitHub branch protection + manual review
