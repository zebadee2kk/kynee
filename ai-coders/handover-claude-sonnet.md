# Handover: Claude Sonnet 4.5

## Profile
- **Strengths**: Production-quality code, debugging, refactoring, algorithm implementation
- **Token Limit**: 200K tokens (1M via API)
- **Session Cost**: Medium (£20/month)
- **Best For**: Agent/console core development, API design, test writing
- **SWE-bench Score**: 62.3% (tied with Opus for complex problem-solving) [web:40]

---

## Current Sprint: Week 3 (Mar 10 - Mar 16, 2026)
**Theme**: Agent v0 (Data Model + Local Collectors)

### Assigned Tasks

#### 1. Agent Core Implementation
- [ ] **Configuration Management** (`agent/aetherpi_agent/config.py`)
  - YAML config loader (using `pyyaml`)
  - Schema: `scope`, `collectors`, `transport`, `audit_log`
  - Validation with Pydantic models
  - Environment variable overrides (12-factor app pattern)

- [ ] **Device Identity** (`agent/aetherpi_agent/identity.py`)
  - Generate UUID on first boot (stored in `/var/lib/aetherpi/device_id`)
  - Enrollment token generation (JWT or symmetric key)
  - Public key export for console pairing

- [ ] **Job Scheduler** (`agent/aetherpi_agent/scheduler.py`)
  - APScheduler integration (cron-style jobs)
  - Job queue (priority, rate limiting)
  - Execution logging (start/stop/duration)
  - Graceful shutdown (SIGTERM handler)

#### 2. Collection Adapters
- [ ] **Network Scanner** (`agent/aetherpi_agent/collectors/network.py`)
  - Wrapper for `nmap` (subprocess call)
  - Input: CIDR range, ports, scan type (-sS, -sV, -O)
  - Output: JSON per `schemas/findings.schema.json`
  - Parser: XML → JSON (using `python-libnmap`)

- [ ] **Wireless Scanner** (`agent/aetherpi_agent/collectors/wireless.py`)
  - Wrapper for `airodump-ng` (monitor mode)
  - Input: Interface, channel, duration
  - Output: JSON (SSIDs, BSSIDs, clients, encryption)
  - Parser: CSV → JSON

- [ ] **Bluetooth Scanner** (`agent/aetherpi_agent/collectors/bluetooth.py`)
  - Wrapper for `hcitool scan` / `bluetoothctl`
  - Input: Scan duration, LE vs. Classic
  - Output: JSON (device addresses, names, classes)
  - Parser: stdout → JSON

#### 3. Output Parsers
- [ ] **Parser Base Class** (`agent/aetherpi_agent/parsers/base.py`)
  - Abstract interface: `parse(raw_output: str) -> dict`
  - Validation against JSON Schema
  - Error handling (malformed output)

- [ ] **Nmap Parser** (`agent/aetherpi_agent/parsers/nmap.py`)
  - Use `python-libnmap` library
  - Extract: hosts, ports, services, OS fingerprints

- [ ] **Airodump Parser** (`agent/aetherpi_agent/parsers/airodump.py`)
  - Parse CSV output (access points + clients)
  - Handle multiple CSV files (rotating captures)

#### 4. Audit Logging
- [ ] **Audit Writer** (`agent/aetherpi_agent/auditlog/writer.py`)
  - Append-only log to `/var/lib/aetherpi/audit.log`
  - JSON Lines format (one JSON object per line)
  - Fields: timestamp, engagement_id, operator_id, action, target, outcome
  - Hash chain (each entry includes hash of previous entry)

#### 5. Systemd Integration
- [ ] **Service File** (`agent/packaging/systemd/aetherpi-agent.service`)
  - Type=notify (sd_notify support)
  - Restart=on-failure
  - User=aetherpi (dedicated user)
  - Capabilities: CAP_NET_RAW, CAP_NET_ADMIN (for raw sockets)

- [ ] **Timer File** (`agent/packaging/systemd/aetherpi-agent.timer`)
  - OnBootSec=5min (delay after boot)
  - OnUnitActiveSec=1h (run every hour)

#### 6. Unit Tests
- [ ] **Test Suite** (`agent/tests/`)
  - `test_config.py`: Config loading, validation
  - `test_identity.py`: UUID generation, enrollment
  - `test_collectors.py`: Mock subprocess calls, verify JSON output
  - `test_parsers.py`: Feed known tool outputs, assert correct JSON
  - `test_auditlog.py`: Verify hash chain integrity
  - Coverage target: >80%

---

## Context

**Project State**:
- Week 1: ADRs completed (Python chosen, JSON + schema validation)
- Week 2: Raspberry Pi 3 image built, hardened, tested
- Week 3 (current): Build agent skeleton + collectors

**Your Mission**:
- Implement the agent as a production-ready systemd service
- Ensure all outputs conform to JSON schemas
- Write comprehensive tests (this code will run unattended)

**Why You**:
- Your coding ability (62.3% SWE-bench) ideal for complex logic
- 200K tokens sufficient for full agent codebase (~5-8K lines)
- Strong debugging skills for parser edge cases

---

## Files to Create

```
agent/
├── aetherpi_agent/
│   ├── __init__.py
│   ├── config.py
│   ├── identity.py
│   ├── scheduler.py
│   ├── collectors/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── network.py
│   │   ├── wireless.py
│   │   └── bluetooth.py
│   ├── parsers/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── nmap.py
│   │   └── airodump.py
│   └── auditlog/
│       ├── __init__.py
│       └── writer.py
├── packaging/systemd/
│   ├── aetherpi-agent.service
│   └── aetherpi-agent.timer
├── tests/
│   ├── test_config.py
│   ├── test_identity.py
│   ├── test_collectors.py
│   ├── test_parsers.py
│   └── test_auditlog.py
├── pyproject.toml
└── README.md
```

---

## Reference Schemas

**You must validate outputs against these** (to be created by Haiku in Week 1):

- `schemas/findings.schema.json` — Network scan results
- `schemas/inventory.schema.json` — Asset inventory
- `schemas/auditlog.schema.json` — Audit events

**Example Finding** (your collectors must output this structure):

```json
{
  "finding_id": "uuid-here",
  "timestamp": "2026-03-15T14:32:01Z",
  "engagement_id": "ENG-2026-042",
  "type": "network_scan",
  "severity": "info",
  "target": "10.0.5.23",
  "details": {
    "hostname": "webserver.local",
    "ports": [
      {"port": 22, "state": "open", "service": "ssh", "version": "OpenSSH 8.2"},
      {"port": 80, "state": "open", "service": "http", "version": "nginx 1.18.0"}
    ]
  }
}
```

---

## Success Criteria

- [ ] Agent starts via `systemctl start aetherpi-agent`
- [ ] Config loads from `/etc/aetherpi/agent.yaml`
- [ ] Scheduled scan executes and outputs valid JSON
- [ ] All tests pass: `pytest tests/ --cov=aetherpi_agent --cov-report=term-missing`
- [ ] Audit log written to `/var/lib/aetherpi/audit.log` with hash chain
- [ ] No hardcoded credentials (all via config)
- [ ] Linting passes: `ruff check .` and `black --check .`

---

## Constraints

**Token Budget**:
- This sprint: ~150K tokens (agent core + collectors + tests)
- If exceeding, prioritize: core → collectors → tests → docs

**Time Estimate**:
- 8-12 hours of development
- Can span multiple sessions (save context between)

**Dependencies**:
- JSON schemas (Haiku should create by Mar 9)
- ADR-001, ADR-003 (architecture decisions from Opus)

---

## Blockers

None currently. If JSON schemas not ready by Mar 10, create minimal versions inline.

---

## Notes for Next Session (Week 4)

**Continuation Tasks**:
- Week 4 focus shifts to **transport** (WireGuard, console API client)
- You'll implement `agent/aetherpi_agent/transport/` module
- Preserve context: config structure, identity format, audit log schema

**Code Quality Checklist**:
- Use type hints (`from typing import ...`)
- Docstrings (Google style) for all public functions
- Exception handling (never let agent crash silently)
- Logging (use Python `logging` module, not `print()`)

---

## Handoff to Other AIs

**After completing this sprint**:

→ **GitHub Copilot**: Assist with unit test generation (inline in VSCode)  
→ **Haiku**: Create default `agent.yaml` config file  
→ **ChatGPT**: Write `agent/README.md` installation guide  

---

**Status**: 🔵 QUEUED (starts Mar 10)  
**Last Updated**: February 24, 2026  
**Next Review**: March 16, 2026 (end of Week 3)
