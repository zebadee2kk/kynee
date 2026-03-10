# AI Session Handover — KYNEĒ (kynee)

> Update this file at the end of every significant AI work session.
> For full technical context, see `WEEK2_COMPLETION_REVIEW.md` and `NEXT_DEVELOPER_START_HERE.md`.

## Last Updated

2026-03-10 — AI documentation layer added (portfolio compliance sweep)

## Current State Summary

KYNEĒ is at end of Week 2 (90% complete). Core infrastructure is solid: PolicyEngine, AuditLogWriter, AgentCoordinator all built and tested (74 tests, 81.98% coverage). CLI is scaffolded but not implemented. Collectors (the core functional value) are not yet started. Week 3 is the next milestone.

## What Was Done This Session

- ✅ Added `ai/AI_CONTEXT.md` — repo orientation
- ✅ Added `ai/AI_RULES.md` — Python/security AI rules
- ✅ Added `ai/AI_HANDOVER.md` — this file
- ✅ Added `PROJECT_STATUS.md` — current priorities
- ✅ Added `ARCHITECTURE.md` — architecture overview

## Active Work Items

1. **CLI implementation** — `agent/kynee_agent/cli/main.py` — 4 commands: `create`, `plan`, `list`, `status` (2-3 days)
2. **Network collector** — `agent/kynee_agent/collectors/network.py` — nmap wrapper (Week 3)
3. **Wireless collector** — `agent/kynee_agent/collectors/wireless.py` — airodump-ng wrapper (Week 3)
4. **Bluetooth collector** — `agent/kynee_agent/collectors/bluetooth.py` — hcitool wrapper (Week 3)

## Known Issues / Blockers

- Python 3.12+ datetime deprecation warnings in mypy — use `# type: ignore` for now
- CLI not yet wired to AgentCoordinator

## Next Session Starting Point

1. Read `NEXT_DEVELOPER_START_HERE.md` (choose path: CLI, Collectors, or Parallel)
2. Read `WEEK2_COMPLETION_REVIEW.md` for detailed implementation specs
3. Run `cd agent && pytest tests/unit/ -v` to verify clean state (should see 74 passing)
4. Create feature branch and begin implementation

## Handover Notes for Specific AI Tools

**Claude Desktop / Claude Code:** Full CLI and collector specs are in `WEEK2_COMPLETION_REVIEW.md`. PolicyEngine and AuditLogWriter patterns are in `agent/tests/unit/` as examples.

**GitHub Copilot:** Standing instructions in `.github/copilot-instructions.md`. Claude instructions in `.claude/`. Always validate policy before scan operations.

**Perplexity:** Use GitHub MCP to read existing code patterns before recommending. The existing test suite is the best reference for correct patterns.
