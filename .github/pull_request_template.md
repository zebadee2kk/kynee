## Scope
<!-- Check ONE primary area -->
- [ ] Agent (`agent/`)
- [ ] Console Backend (`console/backend/`)
- [ ] Console Frontend (`console/frontend/`)
- [ ] Documentation (`docs/`)
- [ ] Infrastructure (`infra/`, Docker, CI/CD)
- [ ] Hardware (`hardware/`)
- [ ] Schemas (`schemas/`)

---

## Owner
<!-- AI agent name or GitHub username -->
**Owner**: <!-- e.g., AI-Agent-Alpha or @username -->

---

## Description
### What changed?
<!-- Brief summary of changes -->

### Why?
<!-- Motivation, related issue, or roadmap milestone -->

**Closes**: #<!-- issue number, if applicable -->

---

## Tests
### Commands Run
```bash
# Paste commands here
```

### Results
<!-- e.g., "All tests passed (42/42)" or "Coverage: 87%" -->

---

## Risk Assessment
<!-- Check one -->
- [ ] **Low** — New feature, no changes to existing code, well-tested
- [ ] **Medium** — Modifies existing code, potential for side effects
- [ ] **High** — Core logic changes, security-sensitive, or breaking changes

### Reasoning
<!-- Explain risk level -->

---

## Overlap & Conflicts
### Files/Areas Touched
<!-- List key files modified -->
- `agent/aetherpi_agent/collectors/network.py` (new file)
- `agent/tests/test_network_collector.py` (new file)
- `docs/architecture/agent-design.md` (updated)

### Potential Conflicts
<!-- Are there other open PRs touching these files? -->
- [ ] No conflicts expected
- [ ] May conflict with PR #<!-- number --> (coordinate with owner)

---

## Checklist
<!-- All items must be checked before requesting review -->

### Code Quality
- [ ] Tests pass locally (`pytest`, `npm test`, or equivalent)
- [ ] Linting applied (`ruff check`, `eslint`, etc.)
- [ ] Formatting applied (`black`, `prettier`, etc.)
- [ ] No commented-out code or TODOs (or filed follow-up issues)

### Documentation
- [ ] Documentation updated (if behavior changes)
- [ ] API docs updated (if endpoints/schemas change)
- [ ] README or other user-facing docs updated (if needed)

### Compliance
- [ ] Conventional commits used (`feat(agent):`, `fix(console):`, etc.)
- [ ] No version number changes (unless authorized by maintainers)
- [ ] Schemas validated (if touching `schemas/*.schema.json`)
- [ ] Rebased onto latest `main`

### Ethics & Security
- [ ] Changes comply with [Ethical Use Policy](../ETHICAL_USE_POLICY.md)
- [ ] No hardcoded secrets or credentials
- [ ] Audit logging added for security-sensitive actions

---

## Additional Notes
<!-- Anything reviewers should know? -->

---

## For Maintainers
<!-- Maintainers fill this section during review -->

### Review Checklist
- [ ] Code review complete
- [ ] Tests adequate
- [ ] Documentation sufficient
- [ ] Security considerations addressed
- [ ] Ready to merge

### Merge Strategy
- [ ] Squash and merge (preferred for feature branches)
- [ ] Rebase and merge (for clean commit history)
- [ ] Merge commit (for release branches only)
