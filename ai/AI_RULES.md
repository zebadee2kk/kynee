# AI Rules — KYNEĒ (kynee)

These rules apply to ALL AI assistants (Claude, Copilot, Perplexity, Cursor, etc.) working in this repository.

## Non-Negotiable Rules

1. **Read before write** — always read existing files before modifying them
2. **Run tests before committing** — `cd agent && pytest tests/unit/ -v --cov=kynee_agent` must pass
3. **No secrets in commits** — never commit API keys, tokens, or credentials
4. **Follow existing patterns exactly** — this codebase has a high quality bar (type hints, async, docstrings)
5. **PolicyEngine first** — EVERY scan operation must validate with PolicyEngine before execution
6. **AuditLogWriter always** — EVERY scan operation must log before execution
7. **Never bypass the schema** — all collector output must match `schemas/findings.schema.json`

## Security Rules

- KYNEĒ is a scanning tool — it must never operate outside its policy constraints
- Never implement collectors that auto-execute without policy validation
- Scan targets must always be validated against allowed ranges in policy config
- Bluetooth and wireless collectors require explicit authorisation scope in policy

## Code Quality Rules

- Python 3.11+ only
- Full type hints on every function signature
- `async`/`await` for all I/O operations — never blocking `subprocess.run`
- Docstrings on every public method
- Formatting: `black .`
- Linting: `ruff check .`
- Type checking: `mypy .`
- Coverage: `>80%` per module

## Collector Development Rules

- Create new collector in `agent/kynee_agent/collectors/<name>.py`
- Return type must be `list[dict[str, Any]]` matching `schemas/findings.schema.json`
- Constructor must accept `policy_engine: PolicyEngine` and `audit_log: AuditLogWriter`
- Validate with `self.policy_engine.validate_scan_request(method, target)` before any scan
- Log with `self.audit_log.log_scan_started(agent_id, scan_id, method, target)` before any scan
- Create paired test file: `tests/unit/test_<name>_collector.py`

## Commit Message Format

```
<type>(<scope>): <description>
```

Types: `feat` | `fix` | `docs` | `test` | `chore` | `refactor`  
Examples: `feat(collectors): add network scanner`, `test(policy): add validation edge cases`

## Before Every Commit Checklist

```bash
cd agent
black .
ruff check .
mypy .
pytest tests/unit/ -v --cov=kynee_agent
```

- [ ] All tests pass (74+ passing)
- [ ] Coverage >80%
- [ ] No type errors (mypy clean)
- [ ] Formatting and linting pass
- [ ] New modules have paired test files
- [ ] `ai/AI_HANDOVER.md` updated if significant session
