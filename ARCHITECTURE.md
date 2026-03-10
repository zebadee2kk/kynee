# Architecture — KYNEĒ (kynee)

> For full technical detail, see `WEEK2_COMPLETION_REVIEW.md` and `WEEK2_HANDOVER.md`.
> For Architecture Decision Records, see `docs/architecture/`.

## Overview

KYNEĒ is a policy-governed, audit-logged network security scanning agent. Every scan request passes through a PolicyEngine before execution, every operation is logged to an AuditLogWriter, and all findings conform to a versioned JSON schema. The core is async Python 3.11+, designed for extensibility via a collector plugin model.

## Key Design Principles

1. **Policy-first** — no scan executes without PolicyEngine.validate_scan_request()
2. **Immutable audit trail** — every operation logged before execution via AuditLogWriter
3. **Schema-enforced output** — all findings match `schemas/findings.schema.json`
4. **Async throughout** — asyncio.create_subprocess_exec for all external tool calls
5. **Type-safe** — full type hints, mypy clean

## Module Overview

```
kynee/
├── agent/
│   ├── kynee_agent/
│   │   ├── core/
│   │   │   ├── policy.py              ← PolicyEngine (built ✅)
│   │   │   ├── audit.py               ← AuditLogWriter (built ✅)
│   │   │   └── coordinator.py         ← AgentCoordinator (built ✅)
│   │   ├── collectors/
│   │   │   ├── network.py             ← nmap wrapper (❌ not built)
│   │   │   ├── wireless.py            ← airodump-ng wrapper (❌ not built)
│   │   │   └── bluetooth.py           ← hcitool wrapper (❌ not built)
│   │   └── cli/
│   │       └── main.py                ← Scaffolded, not implemented (⏸️)
│   └── tests/unit/                    ← 74 tests, 81.98% coverage
├── schemas/
│   └── findings.schema.json           ← CANONICAL output schema
├── docs/architecture/               ← ADR-001 to ADR-004
└── ai-coders/                       ← AI coder configs
```

## Data Flow

```
[User / CLI]
     │
     ▼
[AgentCoordinator]
     │
     ├── PolicyEngine.validate_scan_request(method, target)
     │       └── REJECT if not authorised
     │
     ├── AuditLogWriter.log_scan_started(agent_id, scan_id, method, target)
     │
     ├── Collector.scan(target)
     │     └── nmap / airodump-ng / hcitool
     │
     ├── AuditLogWriter.log_scan_completed(scan_id, result)
     │
     └── Return findings (matches schemas/findings.schema.json)
```

## Testing

```bash
# Install
cd agent && pip install -e ".[dev]"

# Run tests
pytest tests/unit/ -v --cov=kynee_agent

# Full quality check
black . && ruff check . && mypy . && pytest tests/unit/ -v
```

## Collector Contract

Every collector must:

| Requirement | Detail |
|-------------|--------|
| Validate first | `self.policy_engine.validate_scan_request(method, target)` |
| Log first | `self.audit_log.log_scan_started(agent_id, scan_id, method, target)` |
| Async I/O | `asyncio.create_subprocess_exec` only |
| Schema conformance | Return `list[dict]` matching `schemas/findings.schema.json` |
| Type hints | Full signatures with `dict[str, Any]` |
| Test coverage | >80% per collector module |
