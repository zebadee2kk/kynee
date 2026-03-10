# AI Context — KYNEĒ (kynee)

> **Read this first.** This file orients any AI assistant to this repository.
> KYNEĒ has extensive handover documents — use this file to navigate them.

## Repository Purpose

**KYNEĒ** is an AI-governed, policy-enforced network scanning and security assessment agent framework. It runs network, wireless, and Bluetooth scans through a modular collector system, validates every scan against a PolicyEngine before execution, logs all operations to an immutable AuditLogWriter, and produces JSON findings conforming to `schemas/findings.schema.json`.

Target use: cybersecurity consultants, pentest-adjacent tooling, homelab security assessment.

## Start Here — Documentation Navigation

| Document | What It Contains | When to Read |
|----------|------------------|--------------|
| [`NEXT_DEVELOPER_START_HERE.md`](../NEXT_DEVELOPER_START_HERE.md) | ⭐ Current status, setup, three development paths | **Always first** |
| [`WEEK2_COMPLETION_REVIEW.md`](../WEEK2_COMPLETION_REVIEW.md) | Full Week 2 assessment, detailed dev paths | Before starting work |
| [`WEEK2_HANDOVER.md`](../WEEK2_HANDOVER.md) | Technical guide to core modules | Reference |
| [`ROADMAP.md`](../ROADMAP.md) | 8-week development plan | For planning |
| [`HANDOVER.md`](../HANDOVER.md) | Week 1-2 summary | Historical |
| [`PROJECT_STATUS.md`](../PROJECT_STATUS.md) | Current priorities | Each session |
| `docs/architecture/` | 4 Architecture Decision Records | Architecture reference |

## Current Development State (as at 2026-03-10)

- ✅ **Week 1**: Governance, schemas, CI/CD — 100% complete
- ✅ **Week 2**: PolicyEngine, AuditLogWriter, AgentCoordinator — 90% complete
- ⏸️ **CLI**: Scaffolded but NOT yet implemented (`agent/kynee_agent/cli/main.py`)
- ❌ **Collectors**: Not started — Week 3 priority (network, wireless, Bluetooth)
- ✅ **Tests**: 74 passing, 81.98% coverage
- ✅ **CI/CD**: Active

**Active branch model:** `main` is stable. Feature branches: `feature/<name>`.

## Architecture Overview

```
kynee/
├── ai/                                 ← AI context files (YOU ARE HERE)
├── agent/
│   ├── kynee_agent/
│   │   ├── core/
│   │   │   ├── policy.py              ← PolicyEngine — validates ALL scan requests
│   │   │   ├── audit.py               ← AuditLogWriter — immutable audit trail
│   │   │   └── coordinator.py         ← AgentCoordinator — orchestrator
│   │   ├── collectors/            ← ❌ NOT BUILT — Week 3 priority
│   │   │   ├── network.py             ← nmap wrapper
│   │   │   ├── wireless.py            ← airodump-ng wrapper
│   │   │   └── bluetooth.py           ← hcitool wrapper
│   │   └── cli/
│   │       └── main.py                ← ⏸️ Scaffolded, NOT yet implemented
│   └── tests/unit/                    ← 74 tests, 81.98% coverage
├── schemas/
│   └── findings.schema.json           ← ⭐ All collectors MUST match this schema
├── docs/architecture/               ← 4 ADRs
├── .claude/                         ← Claude standing instructions
├── .github/workflows/               ← CI/CD
└── console/, hardware/, infra/      ← Console UI, hardware docs, infrastructure
```

## Mandatory Patterns (non-negotiable)

See `ai/AI_RULES.md` and `NEXT_DEVELOPER_START_HERE.md` for full detail.

1. **PolicyEngine validation before every scan** — no exceptions
2. **AuditLogWriter log call before every scan** — no exceptions
3. **Type hints on every function** (`async def scan(self, target: dict[str, Any]) -> dict[str, Any]`)
4. **Async for all I/O** — `asyncio.create_subprocess_exec`, never `subprocess.run`
5. **Output matches `schemas/findings.schema.json`**
6. **Test coverage >80% per new module**

## Key Relationships

| Repo | Relationship |
|------|--------------|
| `portfolio-management` | Governance hub — tracks this repo's status |
| `sentinelforge` | Threat intelligence layer — may consume KYNEĒ findings |
| `hamnet` | Infrastructure context — KYNEĒ may run scans in homelab |
