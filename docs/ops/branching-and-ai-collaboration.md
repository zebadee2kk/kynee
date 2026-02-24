# Branching & AI Collaboration Guidelines

## Purpose

This document establishes strict branching, versioning, and collaboration rules to enable multiple AI agents and human contributors to work in parallel without conflicts.

---

## Branching Model

### Protected Branches

#### `main`
- **Protected**: Direct pushes disabled
- **Merges**: Only via Pull Requests (PRs) with required checks
- **Status**: Always releasable, deployable
- **CI/CD**: Runs full test suite, security scans, linting

#### `release/x.y`
- **Purpose**: Maintenance branches for released versions
- **Creation**: Cut from `main` when tagging a release (e.g., `v0.9.0` → `release/0.9`)
- **Changes**: Only bug fixes (no new features)
- **Merges**: Cherry-picked fixes merge back into `main` via PR

### Working Branches

**Naming Convention**:
```
<type>/<area>-<short-description>
```

**Types**:
- `feat/` — New features
- `fix/` — Bug fixes
- `docs/` — Documentation changes
- `chore/` — Maintenance (dependencies, config)
- `test/` — Test additions/improvements
- `refactor/` — Code restructuring (no behavior change)

**Areas**:
- `agent` — Agent codebase
- `console-backend` — Console backend
- `console-frontend` — Console frontend
- `infra` — Infrastructure/deployment
- `docs` — Documentation
- `hardware` — Hardware specifications

**Examples**:
```
feat/agent-network-collector
feat/console-backend-auth
feat/console-frontend-dashboard
fix/agent-wireguard-timeout
docs/architecture-adr-updates
chore/deps-update-fastapi
```

---

## AI Agent Collaboration Rules

### 1. Single-Area Ownership

**Rule**: Each branch is owned by **ONE** AI agent or human at a time.

**Ownership Declaration** (in PR description):
```markdown
**Owner**: AI-Agent-Architecture  
**Area**: docs/architecture  
**Duration**: 2026-02-24 to 2026-02-25  
```

**Enforcement**:
- Check open PRs before creating a new branch in the same area
- If conflict: Coordinate in PR comments or wait for merge

### 2. Area Scoping

**Rule**: Each AI agent must work within assigned boundaries.

| AI Agent Role | Allowed Paths | Forbidden Paths |
|---------------|---------------|------------------|
| **Architecture AI** | `docs/architecture/*`, `schemas/*` | Code implementation |
| **Agent Platform AI** | `agent/*`, `scripts/image-build/*`, `docs/build/*` | Console, frontend |
| **Agent Features AI** | `agent/aetherpi_agent/*`, `agent/tests/*` | Console, docs (except API docs) |
| **Console Backend AI** | `console/backend/*`, `docs/api/*` | Agent, frontend |
| **Console Frontend AI** | `console/frontend/*` | Backend, agent |
| **AI/LLM Integration AI** | `console/backend/app/ai/*` | Other backend modules |
| **Infra/DevOps AI** | `infra/*`, `.github/*`, `docker-compose.yml` | Application code |

**Cross-area changes** require:
1. Coordination comment in GitHub Discussions
2. Approval from area owner
3. Documentation in PR description

### 3. Branch Lifetime

**Rule**: Branches must be short-lived.

- **Target**: ≤ 2 days from creation to merge
- **Maximum**: 5 days (after which branch is stale)
- **Stale branches**: Auto-closed by bot (with 24-hour warning)

**Rationale**: Reduces merge conflicts, speeds integration.

### 4. Sequential Dependencies

**Rule**: For structural changes, work sequentially.

**Example**:
- Week 2: Agent Platform AI creates `agent/` structure → merge
- Week 3: Agent Features AI builds on merged structure → merge
- Week 4: Agent Features AI adds transport → merge

**DO NOT**:
- Branch from another agent's unmerged branch
- Create parallel structural changes in the same path

**Exception**: Independent features (e.g., `agent/collectors/network.py` and `agent/collectors/bluetooth.py`) can proceed in parallel if they don't touch shared files.

### 5. Rebase-Before-Merge

**Rule**: Keep branches up-to-date with `main`.

**Process**:
```bash
git fetch origin
git checkout feat/your-branch
git rebase origin/main
# Resolve conflicts if any
git push --force-with-lease
```

**When**: Before marking PR as "Ready for Review"

**CI Enforcement**: PRs with merge conflicts are blocked.

### 6. Conventional Commits

**Rule**: All commits must follow [Conventional Commits](https://www.conventionalcommits.org/).

**Format**:
```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

**Examples**:
```
feat(agent): add network scanner collector
fix(console): resolve CSRF token validation bug
docs(legal): clarify RoE authorization language
test(transport): add WireGuard handshake integration tests
chore(deps): update FastAPI to 0.110.0
```

**Types**:
- `feat` — New feature
- `fix` — Bug fix
- `docs` — Documentation
- `test` — Tests
- `refactor` — Code change (no behavior change)
- `perf` — Performance improvement
- `chore` — Maintenance
- `ci` — CI/CD changes

**Breaking Changes**:
```
feat(api)!: change findings schema to v2

BREAKING CHANGE: `findings.severity` now uses CVSS scores instead of text labels.
```

**Enforcement**: CI checks commit messages via `commitlint`.

### 7. Required Checks (All PRs)

**Automated**:
- [ ] Linting passes (Ruff for Python, ESLint for JS/TS)
- [ ] Tests pass (pytest for Python, Jest for JS/TS)
- [ ] Security scan passes (Bandit, npm audit)
- [ ] No merge conflicts with `main`
- [ ] Commit messages follow Conventional Commits

**Manual** (Reviewer):
- [ ] Code matches area scope
- [ ] Documentation updated (if user-facing)
- [ ] No TODOs or commented-out code
- [ ] Audit logging added (for agent actions)

### 8. Conflict Resolution

**If two AI agents touch the same file**:

1. **First to open PR**: Continues
2. **Second AI**: Must wait for first PR to merge, then rebase
3. **Emergency**: Tag `@zebadee2kk` in both PRs for arbitration

**Preventive**:
- Check open PRs before starting work
- Declare intent in GitHub Discussions (`#week-X-planning`)
- Use draft PRs to signal "work in progress"

---

## Version Control & Releases

### Semantic Versioning

**Format**: `MAJOR.MINOR.PATCH`

- `MAJOR`: Breaking changes (e.g., `1.0.0` → `2.0.0`)
- `MINOR`: New features (backward-compatible) (e.g., `0.5.0` → `0.6.0`)
- `PATCH`: Bug fixes (e.g., `0.9.0` → `0.9.1`)

**Pre-1.0**:
- `0.y.z` indicates beta/unstable
- Breaking changes allowed in `MINOR` (e.g., `0.5.0` → `0.6.0`)

**Version Locations**:
- `agent/pyproject.toml` → `version = "0.1.0"`
- `console/backend/pyproject.toml` → `version = "0.1.0"`
- `console/frontend/package.json` → `"version": "0.1.0"`

### Release Process

**Who**: Only `@zebadee2kk` (maintainer) creates releases.

**Steps**:
1. Update version numbers in all `pyproject.toml`, `package.json`
2. Update `CHANGELOG.md` (using Conventional Commits history)
3. Commit: `chore(release): bump version to 0.9.0`
4. Tag: `git tag -a v0.9.0 -m "Release v0.9.0 - Beta"`
5. Push: `git push origin main --tags`
6. GitHub Actions builds release artifacts (deb, Docker images)
7. Create GitHub Release with notes

**Release Branch** (for bug fixes):
```bash
git checkout -b release/0.9 v0.9.0
# Apply fixes
git commit -m "fix(agent): resolve crash on empty config"
git tag -a v0.9.1 -m "Release v0.9.1 - Patch"
git push origin release/0.9 --tags
# Merge fix back into main
git checkout main
git merge release/0.9
```

### AI Agents and Versioning

**Rule**: AI agents **MUST NOT** bump version numbers.

**Exception**: If instructed explicitly by maintainer:
```
@AI-Agent-Infra: Bump console backend to 0.5.0 and update changelog
```

---

## PR Template

**All PRs must include**:

```markdown
## Description
[Brief summary of changes]

## Type
- [ ] Feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Refactoring
- [ ] Infrastructure

## Area
- [ ] Agent
- [ ] Console Backend
- [ ] Console Frontend
- [ ] Documentation
- [ ] Infrastructure

## Owner
**Owner**: [AI-Agent-Name or @github-username]  
**Duration**: [Start date] to [Expected merge date]  

## Testing
**Commands run**:
```bash
pytest tests/
ruff check .
black --check .
```

**Results**: ✅ All tests pass

## Risk Assessment
- [ ] Low (cosmetic, docs, tests)
- [ ] Medium (new feature, refactoring)
- [ ] High (breaking change, security-critical)

## Overlap Potential
**Files/areas that may conflict with other branches**:
- None / [List files]

## Checklist
- [ ] Conventional Commits followed
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No TODOs or dead code
- [ ] Audit logging added (if agent action)
- [ ] Rebased on latest `main`
- [ ] All CI checks pass
```

---

## Communication Channels

### GitHub Discussions

- **Planning**: `#week-X-planning` (declare work for the week)
- **Coordination**: `#ai-agent-coordination` (resolve conflicts)
- **Questions**: `#q-and-a`

### PR Comments

- Tag other AI agents if coordination needed: `@AI-Agent-Console-Backend`
- Use `LGTM` (Looks Good To Me) to approve
- Use `Request Changes` for blocking issues

### Issues

- Create issues for discovered bugs
- Link PRs to issues: `Fixes #42`, `Closes #123`

---

## Examples

### Good: Clean separation

**PR #1** (AI-Agent-Platform):
- Branch: `feat/agent-platform-kali-rpi3`
- Files: `scripts/image-build/*`, `docs/build/*`
- No conflicts

**PR #2** (AI-Agent-Features, after #1 merged):
- Branch: `feat/agent-collectors-network`
- Files: `agent/aetherpi_agent/collectors/network.py`
- No conflicts

### Bad: Overlapping work

**PR #1** (AI-Agent-A):
- Branch: `feat/agent-all-collectors`
- Files: `agent/aetherpi_agent/collectors/*.py` (all at once)

**PR #2** (AI-Agent-B, opened before #1 merged):
- Branch: `feat/agent-bluetooth-collector`
- Files: `agent/aetherpi_agent/collectors/bluetooth.py`
- **Conflict**: Both modify the same area

**Resolution**: AI-Agent-B waits for #1 to merge, then rebases.

---

## Summary

| Rule | Enforcement |
|------|-------------|
| Single-area ownership | Manual (PR review) |
| Conventional Commits | CI (`commitlint`) |
| Tests pass | CI (pytest, Jest) |
| No merge conflicts | CI (GitHub) |
| Branch lifetime ≤5 days | Bot (auto-close) |
| Version bumps by maintainer only | Manual (PR review) |

---

**Last Updated**: February 24, 2026  
**Maintained By**: @zebadee2kk
