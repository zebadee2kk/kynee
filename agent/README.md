# KYNEĒ Agent

The KYNEĒ agent runs on a Raspberry Pi and performs authorized data collection during a security assessment. It reports findings back to the console and records immutable audit logs.

**Important:** Use only with written authorization. See [ETHICAL_USE_POLICY.md](../ETHICAL_USE_POLICY.md).

---

## 📋 Overview

The agent is responsible for:
- **Data collection**: Network scanning, wireless reconnaissance, Bluetooth enumeration, physical security testing
- **Policy enforcement**: Respects scope boundaries, rate limits, authorized methods
- **Audit logging**: Immutable cryptographic hash-chained logs
- **Console communication**: Secure WireGuard VPN with HTTPS fallback
- **Minimal footprint**: ~30-50MB Python runtime on 1GB Raspberry Pi 3

**Status**: Pre-Alpha (Week 1-2 scaffolding complete, Week 3-4 collectors in progress)

---

## 🛠️ Developer Setup

### Prerequisites

- Python 3.11+ (test with pyenv or docker)
- pip/uv for dependency management
- Git 2.40+

### Clone & Install

```bash
# Clone repo (if not already done)
git clone https://github.com/zebadee2kk/kynee.git
cd kynee/agent

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Format and lint
black .
ruff check . --fix
mypy .
```

### Project Structure

```
agent/
├── pyproject.toml              # Package metadata, dependencies, tool config
├── kynee_agent/
│   ├── __init__.py
│   ├── core/
│   │   ├── agent.py           # Main Agent class (lifecycle management)
│   │   └── __init__.py
│   ├── models/                # Pydantic models (Finding, Engagement, InventoryItem)
│   │   ├── finding.py
│   │   ├── engagement.py
│   │   ├── inventory.py
│   │   └── __init__.py
│   ├── collectors/            # Data collection modules (network, wireless, BT)
│   │   └── __init__.py
│   ├── transport/             # WireGuard + HTTPS communication
│   │   └── __init__.py
│   ├── policy/                # Scope validation, rate limiting
│   │   └── __init__.py
│   ├── audit/                 # Hash-chained immutable logging
│   │   └── __init__.py
│   └── cli/                   # Command-line interface
│       ├── main.py
│       └── __init__.py
└── tests/
    ├── unit/                  # Unit tests
    │   └── test_agent.py
    ├── integration/           # Integration tests (hardware-dependent)
    └── conftest.py           # Pytest fixtures
```

### Key Classes & APIs

#### Agent (core/agent.py)

```python
from kynee_agent.core import Agent

# Initialize
agent = Agent(agent_id="my-agent-001", config_path="/etc/kynee/agent.yaml")

# Lifecycle
await agent.start()   # Load RoE, connect to console, start collectors
await agent.stop()    # Graceful shutdown

# Operations
findings = await agent.execute_scan(job={"target": "10.0.0.0/24", "tool": "nmap"})
status = agent.get_status()  # Heartbeat
```

#### Models

```python
from kynee_agent.models import Finding, Engagement, InventoryItem

# Pydantic models automatically validate against JSON schemas
finding = Finding(
    engagement_id="eng-001",
    agent_id="agent-001",
    title="Open SSH Port",
    description="SSH is publicly accessible",
    category="network",
    severity="medium",
    tool="nmap"
)
```

---

## 🚀 Installation (Target: Week 7)

Packaging is planned for Week 7. Until then, run from source:

```bash
# Development mode
cd agent && python -m kynee_agent.cli.main start --config /etc/kynee/agent.yaml

# Or via pip
pip install -e .
kynee-agent start --config /etc/kynee/agent.yaml
```

---

---

## 📦 Hardware & OS

### Requirements

- **Hardware**: Raspberry Pi 3 Model B+ or better
- **OS**: Kali Linux ARM (2024.1+)
- **Storage**: 32GB+ microSD (Class 10+)
- **Optional**: Wi-Fi adapter (Alfa AWUS036ACH), Bluetooth adapter (Plugable USB-BT4LE)

See [../hardware/bill-of-materials.md](../hardware/bill-of-materials.md) for details.

### Service Management (Coming Week 2)

```bash
# systemd service (to be implemented)
sudo systemctl enable kynee-agent
sudo systemctl start kynee-agent
sudo systemctl status kynee-agent
```

---

## ⚙️ Configuration (Coming Week 3)

Default location: `/etc/kynee/agent.yaml`

Expected keys:
```yaml
console_url: "https://console.example.com"
enrollment_token: "token-xyz"
scan_schedule: "0 */4 * * *"  # Every 4 hours
rate_limits:
  nmap_scans: 1
  wifi_handshakes: 5
```

---

## 📝 Testing

```bash
# Unit tests
pytest tests/unit/ -v

# With coverage
pytest tests/ --cov=kynee_agent --cov-report=html

# Type checking
mypy kynee_agent/

# Linting
ruff check .
black --check .
```

---

## 🔐 Security & Ethics

- **Always** obtain written Rules of Engagement (RoE) before scanning
- Respect scope boundaries (enforced by policy engine)
- Maintain immutable audit logs for legal defensibility
- See [../ETHICAL_USE_POLICY.md](../ETHICAL_USE_POLICY.md)

---

## 📋 Roadmap

| Week | Deliverable | Status |
|------|-------------|--------|
| 1-2 | Project scaffolding, core Agent class | ✅ Complete |
| 3-4 | Collectors (network, wireless, BT), policy engine | ⏳ In Progress |
| 5 | Transport integration (WireGuard/HTTPS) | ⏳ Planned |
| 6 | AI assistant integration | ⏳ Planned |
| 7-8 | Packaging & beta release | ⏳ Planned |

---

## 🤝 Contributing

1. Create branch: `git checkout -b feat/agent-<description>`
2. Make changes and run tests locally
3. Push and open PR (see [../docs/ops/branching-and-ai-collaboration.md](../docs/ops/branching-and-ai-collaboration.md))
4. Address feedback, then merge

---

## 📚 References

- [ADR-0001: Agent Language (Python)](../docs/architecture/adr-0001-agent-language.md)
- [ADR-0002: Transport Design](../docs/architecture/adr-0002-transport.md)
- [ADR-0004: Audit Logging](../docs/architecture/adr-0004-audit-logging.md)
- [Pydantic Documentation](https://docs.pydantic.dev)
- [FastAPI Agent Integration](../docs/ai-assistant.md)
