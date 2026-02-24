# Branching & AI Collaboration Guidelines

## Purpose

This document establishes strict rules for branch management and collaboration to prevent conflicts when multiple AI agents and human developers work in parallel on KYNEĒ.

---

## Branching Model

### Protected Branches

#### `main`
- **Always releasable**
- Direct pushes: **DISABLED**
- Merges: Only via Pull Requests with required checks
- Branch protection:
  - Required reviews: 1+ approvals
  - Required status checks: CI tests, security scan, lint
  - Enforce linear history (squash or rebase)

#### `release/x.y`
- Created from `main` for each minor version (e.g., `release/0.9`)
- Purpose: Bug fixes and patches for that release
- Changes must be cherry-picked back to `main`
- Tagged releases: `v0.9.0`, `v0.9.1`, etc.

### Working Branches (Short-Lived)

All development work happens on topic branches:

**Naming Convention**:
```
<type>/<area>-<description>
```

**Types**:
- `feat/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation only
- `chore/` — Maintenance, refactoring, tooling
- `test/` — Test additions/improvements

**Areas**:
- `agent` — Agent codebase
- `console-backend` — Console backend
- `console-frontend` — Console frontend
- `docs` — Documentation
- `infra` — Infrastructure, CI/CD, Docker
- `hardware` — Hardware guides, BOM

**Examples**:
```
feat/agent-collectors-network
feat/console-backend-engagements-api
feat/console-frontend-findings-table
fix/agent-policy-scope-validation
docs/architecture-adr-transport
chore/infra-ci-security-scanning
```

**Lifetime**: Target <= 2 days, maximum 1 week.

---

## AI Agent Collaboration Rules

### Rule 1: Single-Area Ownership Per Branch

Each branch is owned by **one AI agent or human** and targets **one logical area**.

✅ **Good**:
- `feat/agent-collectors-bluetooth` (AI Agent A, touches only `agent/aetherpi_agent/collectors/bluetooth.py`)
- `feat/console-backend-auth` (AI Agent B, touches only `console/backend/app/auth/`)

❌ **Bad**:
- `feat/agent-and-console-updates` (mixes agent and console changes)
- Branch with changes to `agent/`, `console/`, and `docs/` unrelated to a single feature

### Rule 2: No Concurrent Structural Changes Per Area

For **structural changes** (new modules, file moves, major refactors):

- Only **one open PR per area** at a time
- Other AI agents must wait for merge or coordinate explicitly

**Example**:
- If `feat/agent-scheduler-v0` is open (adding `agent/aetherpi_agent/scheduler.py`), no other agent should create competing scheduler implementations
- For **additive changes** (new collectors, new endpoints), multiple PRs are OK if they touch different files

### Rule 3: Declare Ownership in PR

Every PR **must** include in the description:

```markdown
**Owner**: [AI Agent Name / Human Name]
**Area**: [agent | console-backend | console-frontend | docs | infra | hardware]
**Files Modified**: [count]
**Risk Level**: [Low | Medium | High]
```

### Rule 4: Rebase Before Merge

Before requesting merge:

```bash
git fetch origin
git rebase origin/main
# Resolve conflicts if any
git push --force-with-lease
```

**Why**: Keeps history linear, prevents merge commits.

### Rule 5: Conventional Commits (Mandatory)

All commits must follow [Conventional Commits](https://www.conventionalcommits.org/):

**Format**:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Examples**:
```
feat(agent): add Bluetooth discovery collector
fix(console): handle missing engagement_id in findings API
docs(legal): clarify RoE template scope language
chore(ci): add security scanning workflow
test(agent): add unit tests for policy engine
```

**Scopes** (align with areas):
- `agent`, `console`, `docs`, `infra`, `hardware`, `schemas`

**Breaking changes**:
```
feat(agent)!: redesign collector interface

BREAKING CHANGE: Collectors now require async/await.
```

### Rule 6: No Cross-Area Formatting

AI agents must **not**:

- Run formatters (Black, Prettier) across the entire repo
- Bulk-rename files outside their assigned area
- Change shared configuration files (`.gitignore`, `.editorconfig`) unless explicitly tasked

**Why**: Causes massive merge conflicts.

### Rule 7: Avoid Editing Shared Schemas Concurrently

Files in `schemas/*.schema.json` are shared contracts.

**Process**:
1. Propose schema changes in a **dedicated PR** (e.g., `feat/schemas-findings-v2`)
2. Get approval from maintainer
3. Merge schema changes **first**
4. Then implement dependent features in separate PRs

### Rule 8: Version Numbers Off-Limits for AI Agents

AI agents must **never** modify:

- `pyproject.toml` (version field)
- `package.json` (version field)
- `CHANGELOG.md` (only maintainers add release notes)

Unless explicitly instructed: "Bump version to X.Y.Z."

---

## Pull Request Workflow

### 1. Create Branch

```bash
git checkout main
git pull origin main
git checkout -b feat/agent-collectors-network
```

### 2. Make Changes

- Write code
- Write tests
- Update docs if needed
- Commit with conventional commit messages

### 3. Pre-PR Checklist

- [ ] All tests pass locally
- [ ] Code formatted (Black/Prettier)
- [ ] Lint checks pass (Ruff/ESLint)
- [ ] No merge conflicts with `main`
- [ ] Conventional commit messages
- [ ] Documentation updated (if user-facing change)

### 4. Open Pull Request

Use the PR template (`.github/pull_request_template.md`):

```markdown
## Summary
[Brief description of changes]

## Owner
**Owner**: AI Agent Name / Human Name
**Area**: agent

## Changes
- Added network collector using nmap
- Implemented JSON output per findings schema
- Added unit tests

## Testing
```bash
cd agent
pytest tests/collectors/test_network.py -v
```
All tests pass ✅

## Risk Level
Low — New feature, no changes to existing code

## Files Changed
- `agent/aetherpi_agent/collectors/network.py` (new)
- `agent/tests/collectors/test_network.py` (new)
- `agent/README.md` (updated)

## Related Issues
Closes #42
```

### 5. Address Review Feedback

- Make requested changes
- Commit with conventional messages
- Push updates (no force-push after review starts unless discussed)

### 6. Merge

Maintainer will merge using:

- **Squash and merge** (for small PRs)
- **Rebase and merge** (for clean commit history)

Never use "merge commit" to keep history linear.

---

## Version Control & Releases

### Semantic Versioning (SemVer)

`MAJOR.MINOR.PATCH`

- `0.y.z` — Pre-1.0 (beta), breaking changes allowed
- `1.0.0` — First stable release
- `1.1.0` — New features (backwards-compatible)
- `1.1.1` — Bug fixes (no new features)

### Git Tags

```bash
git tag -a v0.1.0 -m "Week 1 milestone: Governance and schemas"
git push origin v0.1.0
```

### Release Process

1. Maintainer creates release branch: `release/0.9`
2. CI builds artifacts (deb, Docker images)
3. Tag release: `v0.9.0`
4. GitHub Release created with changelog
5. Bug fixes go to `release/0.9`, tagged as `v0.9.1`, merged back to `main`

---

## Conflict Resolution

### Rebase Conflicts

If rebase fails:

```bash
git rebase origin/main
# Fix conflicts in editor
git add <resolved-files>
git rebase --continue
git push --force-with-lease
```

### Overlapping PRs

If two PRs touch the same files:

1. **First PR merged wins**
2. Second PR must rebase and resolve conflicts
3. If conflicts are complex, coordinate in PR comments

### Deadlocks

If multiple AI agents are blocked:

1. Tag maintainer in PR comments
2. Maintainer decides merge order
3. Losing PR rebases after winner merges

---

## CI/CD Integration

### Required Checks (Enforced by Branch Protection)

1. **Lint**:
   - Python: `ruff check`
   - JavaScript: `eslint`

2. **Tests**:
   - Python: `pytest`
   - JavaScript: `npm test`

3. **Security Scan**:
   - `bandit` (Python)
   - `npm audit` (JavaScript)
   - Dependency scanning (Dependabot)

4. **Build**:
   - Agent: `pip install -e .`
   - Console: Docker build

### Workflow Triggers

- **On PR**: Run all checks
- **On push to `main`**: Run checks + build artifacts
- **On tag `v*`**: Release workflow (build, publish, GitHub Release)

---

## Anti-Patterns (Do NOT Do This)

❌ **Mixing unrelated changes in one PR**
- "Fixed bug in agent, added console feature, updated docs"

❌ **Long-lived branches**
- Branches open for weeks accumulate conflicts

❌ **Editing files outside your area**
- Agent AI touching `console/` code

❌ **Committing secrets or test data**
- RoE documents, credentials, packet captures

❌ **Force-pushing after review starts**
- Breaks reviewer context

❌ **Skipping tests**
- "Will add tests later" — No, tests are required

---

## Quick Reference Card

| Action | Command |
|--------|--------|
| Create branch | `git checkout -b feat/area-description` |
| Commit | `git commit -m "feat(area): description"` |
| Push | `git push origin feat/area-description` |
| Update from main | `git fetch && git rebase origin/main` |
| Force push (after rebase) | `git push --force-with-lease` |
| Run tests (Python) | `pytest tests/` |
| Run tests (JS) | `npm test` |
| Lint (Python) | `ruff check .` |
| Lint (JS) | `npm run lint` |
| Format (Python) | `black .` |
| Format (JS) | `npm run format` |

---

## Questions?

- **Branching confusion**: Ask in PR comments, tag `@maintainers`
- **Merge conflicts**: Post conflict details in PR, maintainer will advise
- **AI agent coordination**: Use GitHub Discussions for planning

---

**Last Updated**: February 24, 2026  
**Maintainer**: @zebadee2kk  
**Applies to**: All contributors (humans and AI agents)
