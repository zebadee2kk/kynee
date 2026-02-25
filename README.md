# KYNEĒ (Helm of Hades)

**Ethical Penetration Testing Agent for Authorized Security Assessments**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Ethical%20Use%20Required-red.svg)](ETHICAL_USE_POLICY.md)
[![Status](https://img.shields.io/badge/Status-Pre--Alpha-yellow.svg)](ROADMAP.md)
[![Tests](https://img.shields.io/badge/Tests-74%20Passing-brightgreen.svg)](agent/tests/)
[![Coverage](https://img.shields.io/badge/Coverage-81.98%25-brightgreen.svg)](WEEK2_COMPLETION_REVIEW.md)

KYNEĒ is a Raspberry Pi-based autonomous penetration testing agent designed for authorized security assessments. Named after the Helm of Hades (which granted invisibility in Greek mythology), it combines low-cost hardware with professional security tools for stealthy reconnaissance.

> **⚠️ CRITICAL**: KYNEĒ is designed exclusively for **authorized** penetration testing with written permission. Unauthorized use is illegal and unethical. See [Ethical Use Policy](ETHICAL_USE_POLICY.md).

---

## 🚀 **New Developer? Start Here!**

**Week 2 Complete (90%)** — Ready for Week 3 development!

### Quick Start for Next Developer

1. **Read First**: [📋 NEXT_DEVELOPER_START_HERE.md](NEXT_DEVELOPER_START_HERE.md) — Quick handover guide
2. **Complete Review**: [📊 WEEK2_COMPLETION_REVIEW.md](WEEK2_COMPLETION_REVIEW.md) — Full project assessment
3. **Choose Path**:
   - **Option 1**: Complete CLI (2-3 days) ⭐ Recommended
   - **Option 2**: Begin Collectors (5-7 days) 🔥 Fastest value
   - **Option 3**: Both parallel (1 week) ⚡ Max speed

**Current Status**: Core infrastructure complete (81.98% test coverage, 74 passing tests). CLI scaffolded but not implemented. Collectors ready to begin.

---

## 🎯 Features

### Current Status: **Pre-Alpha Development (Week 2 — 90% Complete)**

See [ROADMAP.md](ROADMAP.md) for the 8-week development plan.

#### ✅ Completed (Week 1-2)

- **Core Infrastructure**: Policy enforcement, hash-chained audit logging, multi-agent coordination
- **Data Models**: Engagement, Finding, Inventory (Pydantic models with full validation)
- **Policy Engine**: Scope validation, time windows, method authorization, rate limiting
- **Audit Logger**: Hash-chained append-only logs with tamper detection
- **Test Suite**: 74 unit tests, 81.98% coverage (exceeds 80% target)
- **CI/CD**: GitHub Actions with linting, type checking, security scanning
- **Documentation**: 4 ADRs, 4 JSON schemas, comprehensive handover guides

#### 🚧 In Progress (Week 2.5)

- **CLI Prototype**: Scaffolded, needs implementation (4 commands)

#### 📋 Planned (Week 3+)

- **Autonomous Network Discovery**: Automated nmap scanning with intelligent target prioritization
- **Wireless Reconnaissance**: WPA/WPA2 handshake capture, rogue AP detection
- **Bluetooth/BLE Analysis**: Device enumeration and service discovery
- **Flipper Zero Integration**: RFID/NFC reading, Sub-GHz analysis, IR capture
- **Secure Console**: Web-based command center with engagement management
- **AI-Powered Suggestions**: LLM-driven recommendations for next steps

---

## 📦 Repository Structure

```
kynee/
├── agent/                  # Raspberry Pi agent codebase (Python)
│   ├── kynee_agent/
│   │   ├── core/          # ✅ Agent, Coordinator, Exceptions
│   │   ├── policy/        # ✅ Policy Engine (RoE enforcement)
│   │   ├── audit/         # ✅ Audit Logger (hash-chained)
│   │   ├── models/        # ✅ Engagement, Finding, Inventory
│   │   ├── collectors/    # ⏳ Week 3 (network, wireless, bluetooth)
│   │   ├── transport/     # ⏳ Week 4 (WireGuard, HTTPS)
│   │   └── cli/           # 🚧 Scaffolded (needs implementation)
│   └── tests/unit/        # ✅ 74 tests, 81.98% coverage
├── console/
│   ├── backend/           # ⏳ Week 5 (FastAPI backend)
│   └── frontend/          # ⏳ Week 5 (React frontend)
├── docs/
│   ├── architecture/      # ✅ 4 ADRs (language, transport, serialization, audit)
│   ├── build/             # ⏳ OS setup, hardening guides
│   ├── ops/               # ✅ Deployment, branching strategy
│   ├── api/               # ⏳ OpenAPI specs
│   └── legal/             # ✅ RoE templates, compliance
├── hardware/              # ✅ BOM, compatibility, Flipper docs
├── schemas/               # ✅ 4 JSON schemas (validated)
├── scripts/               # ✅ Build/provisioning scripts
├── infra/                 # ⏳ Docker, Helm, Terraform, WireGuard
├── examples/              # ✅ Example configs, use cases
├── validation-reports/    # ✅ Codex validation artifacts
└── third_party/licenses/  # ✅ Third-party licenses
```

**Legend**: ✅ Complete | 🚧 In Progress | ⏳ Planned

---

## 🚀 Quick Start

### Prerequisites

- **Hardware**: Raspberry Pi 3 Model B+ or better (see [hardware/bill-of-materials.md](hardware/bill-of-materials.md))
- **OS**: Kali Linux ARM (2024.1+)
- **Optional**: Flipper Zero (for physical security testing)

### Installation (Coming Soon)

```bash
# 1. Flash Kali ARM image to SD card
# See docs/build/kali-rpi3-minimal.md (coming in Week 2)

# 2. Install agent
sudo dpkg -i kynee-agent_0.9.0_armhf.deb

# 3. Enroll agent with console
sudo kynee-agent enroll --console https://console.example.com

# 4. Start engagement (requires Rules of Engagement file)
sudo kynee-agent start --roe engagement-001.roe.json
```

---

## 📚 Documentation

### 🆕 Developer Handover (Week 2 → Week 3)

- **[NEXT_DEVELOPER_START_HERE.md](NEXT_DEVELOPER_START_HERE.md)** — Quick-start guide for next developer ⭐ **READ THIS FIRST**
- **[WEEK2_COMPLETION_REVIEW.md](WEEK2_COMPLETION_REVIEW.md)** — Complete Week 2 assessment with handover prompts
- **[WEEK2_HANDOVER.md](WEEK2_HANDOVER.md)** — Technical guide to core modules
- **[HANDOVER.md](HANDOVER.md)** — Week 1-2 summary and Week 3 preparation

### User Documentation

- [Roadmap](ROADMAP.md) — 8-week development timeline
- [Ethical Use Policy](ETHICAL_USE_POLICY.md) — **READ THIS FIRST**
- [Hardware Guide](hardware/bill-of-materials.md) — Component selection
- [Rules of Engagement Template](docs/legal/rules-of-engagement-template.md) — Authorization framework

### Developer Documentation

- [Contributing Guide](CONTRIBUTING.md) — How to contribute
- [Architecture Decision Records](docs/architecture/adr-0000-index.md) — Technical decisions
- [Branching & AI Collaboration](docs/ops/branching-and-ai-collaboration.md) — Git workflow
- [Code of Conduct](CODE_OF_CONDUCT.md) — Community standards
- [Governance](GOVERNANCE.md) — Project governance
- [Security Policy](SECURITY.md) — Vulnerability reporting

---

## 🛠️ Developer Setup

### Prerequisites

- **Python**: 3.11+ (for agent & console backend)
- **Node.js**: 20+ (for console frontend)
- **Git**: 2.40+
- **VS Code** (recommended) or any editor

### Clone & Setup

```bash
# Clone repository
git clone https://github.com/zebadee2kk/kynee.git
cd kynee

# Install pre-commit hooks (optional)
pip install pre-commit
pre-commit install
```

### Agent Development (Week 2-3)

```bash
# Navigate to agent
cd agent

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests (should see 74 passing)
pytest tests/unit/ -v --cov=kynee_agent

# Expected: 74 passed, 81.98% coverage ✅
```

### VS Code Workspace

Open the multi-root workspace for organized development:

```bash
code .vscode/kynee.code-workspace
```

This loads separate folders for:
- Agent (`agent/`)
- Console Backend (`console/backend/`)
- Console Frontend (`console/frontend/`)
- Docs (`docs/`)
- Hardware (`hardware/`)

With pre-configured settings for Python (Black, Ruff, Pytest) and TypeScript (ESLint, Prettier).

### Branching Strategy

We use a **trunk-based** workflow with short-lived branches:

- `main` — Protected, always releasable
- `feat/<area>-<description>` — New features
- `fix/<area>-<description>` — Bug fixes
- `docs/<area>-<description>` — Documentation

**Critical**: Multiple AI agents and humans collaborate on this repo. See [Branching & AI Collaboration Guidelines](docs/ops/branching-and-ai-collaboration.md) for rules to avoid conflicts.

### Running Tests

```bash
# Agent tests
cd agent
pytest tests/ -v --cov=kynee_agent

# Coverage report
pytest tests/ --cov=kynee_agent --cov-report=html
open htmlcov/index.html

# Console backend tests (when available)
cd console/backend
pytest tests/ -v

# Console frontend tests (when available)
cd console/frontend
npm test
```

### CI/CD

GitHub Actions runs on every PR:

- Linting (Ruff, ESLint)
- Type checking (mypy)
- Tests (pytest, npm test)
- Security scanning (Bandit, Semgrep)
- Schema validation

See [`.github/workflows/`](.github/workflows/) for workflow definitions.

---

## 🔒 Security

### Ethical Use

KYNEĒ is designed for **authorized penetration testing only**. Key principles:

- **Always obtain written authorization** (Rules of Engagement)
- **Never deploy on unauthorized networks**
- **Respect scope boundaries** (automated enforcement)
- **Maintain audit logs** (immutable, cryptographically signed)
- **Follow laws and regulations** (CFAA, GDPR, etc.)

See [ETHICAL_USE_POLICY.md](ETHICAL_USE_POLICY.md) for full policy.

### Reporting Vulnerabilities

**DO NOT** report security issues via GitHub Issues. See [SECURITY.md](SECURITY.md) for responsible disclosure process.

---

## 🤝 Contributing

We welcome contributions! Please:

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)
2. Check [GitHub Issues](https://github.com/zebadee2kk/kynee/issues) for open tasks
3. Follow [branching guidelines](docs/ops/branching-and-ai-collaboration.md)
4. Use conventional commits (`feat:`, `fix:`, `docs:`)
5. Ensure tests pass and linting is clean

**For AI Agents**: See [AI Collaboration Rules](docs/ops/branching-and-ai-collaboration.md#ai-agent-collaboration-rules) for handover sequence and conflict avoidance.

**For Next Developer**: Start with [NEXT_DEVELOPER_START_HERE.md](NEXT_DEVELOPER_START_HERE.md) for Week 3 onboarding.

---

## 📌 Roadmap

Current phase: **Week 2 Complete (90%)** — Ready for Week 3

| Week | Milestone | Status |
|------|-----------|--------|
| 1 | Foundations (governance, schemas, ADRs) | ✅ Complete |
| 2 | Core Modules (policy, audit, coordinator, tests) | 🟢 90% Complete |
| 2.5 | CLI Implementation (4 commands) | 🟡 Scaffolded |
| 3 | Agent Collectors (network, wireless, bluetooth) | ⏳ Ready to Start |
| 4 | Secure Transport (WireGuard, enrollment) | ⏳ Planned |
| 5 | Console v0 (backend + frontend) | ⏳ Planned |
| 6 | AI Assistant Integration | ⏳ Planned |
| 7-8 | Integrations & Beta Release | ⏳ Planned |

See [ROADMAP.md](ROADMAP.md) for detailed milestones and deliverables.

**Week 2 Achievements**:
- ✅ Core modules implemented (exceptions, coordinator, policy, audit)
- ✅ 74 unit tests with 81.98% coverage (exceeds 80% target)
- ✅ Policy engine enforces RoE (scope, time, methods, rate limits)
- ✅ Hash-chained audit logging with tamper detection
- ✅ Multi-agent coordination framework
- ⏸️ CLI scaffolded but not implemented (deferred to Week 2.5)

---

## ⚖️ License

**Apache License 2.0** — See [LICENSE](LICENSE)

### Key Terms

- ✅ **Commercial use allowed**
- ✅ **Modification allowed**
- ✅ **Distribution allowed**
- ✅ **Patent grant included**
- ⚠️ **Liability/warranty disclaimer**

**However**: You MUST comply with [Ethical Use Policy](ETHICAL_USE_POLICY.md). Apache 2.0 grants software rights, but does not authorize illegal use.

---

## 📧 Contact

- **Issues & Questions**: [GitHub Discussions](https://github.com/zebadee2kk/kynee/discussions)
- **Security**: See [SECURITY.md](SECURITY.md)
- **Governance**: See [GOVERNANCE.md](GOVERNANCE.md)

---

## 🔗 Related Projects

- [Kali Linux](https://www.kali.org/) — Base OS
- [Flipper Zero](https://flipperzero.one/) — Hardware companion
- [WireGuard](https://www.wireguard.com/) — Secure transport
- [OWASP](https://owasp.org/) — Security standards

---

## 🙏 Acknowledgments

KYNEĒ builds upon the work of:

- **Kali Linux Team** — Security tool distribution
- **Offensive Security** — Training and methodologies
- **Open-source security community** — Tools and frameworks
- **Codex & Claude AI** — Week 1-2 development contributors

---

**⚠️ Disclaimer**: The developers of KYNEĒ are not responsible for misuse. This tool is provided for lawful, authorized security testing only. Users are solely responsible for compliance with applicable laws.

---

**Project Status**: Pre-Alpha Development (Week 2 — 90% Complete)  
**Version**: 0.2.0-dev  
**Last Updated**: February 25, 2026  
**Maintainer**: [@zebadee2kk](https://github.com/zebadee2kk)
