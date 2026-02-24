# KYNEĒ 🕵️

> *Named after the Helm of Hades (Ἅίδος κυνέη) — the legendary Cap of Invisibility worn by Athena, Hermes, and Perseus to conduct reconnaissance unseen.*

**KYNEĒ** is an AI-assisted portable security assessment platform designed exclusively for licensed penetration testers, red teams, and cybersecurity companies conducting **authorized** security assessments.

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Security](https://img.shields.io/badge/Security-Vulnerability%20Disclosure-red)](SECURITY.md)
[![Code of Conduct](https://img.shields.io/badge/Code%20of%20Conduct-Contributor%20Covenant-4baaaa.svg)](CODE_OF_CONDUCT.md)

## ⚠️ Legal & Ethical Use Only

**This tool is intended ONLY for authorized security assessments with explicit written permission.**

- ✅ Licensed penetration testers with signed Rules of Engagement (RoE)
- ✅ Red team operations with documented authorization
- ✅ Organizations testing their own infrastructure
- ❌ Unauthorized network scanning or access
- ❌ Malicious or illegal activities

See our [**Ethical Use Policy**](ETHICAL_USE_POLICY.md) for complete guidelines.

---

## 🎯 Project Goal

Create a compact, Raspberry Pi 3-based device that security professionals can legally deploy during authorized penetration tests and red-team exercises. The device performs:

- Network discovery and vulnerability auditing
- Wireless and Bluetooth reconnaissance
- Physical-layer testing (via Flipper Zero integration)
- Secure reporting to a central management console
- AI-assisted analysis with human-in-the-loop approval

---

## 📦 System Architecture

```
┌───────────────────────┐
│  Raspberry Pi 3 Agent  │
│  (Kali Linux ARM)     │
│                       │
│  • Network Scanning   │
│  • WiFi/BT Recon      │
│  • Flipper Control    │
│  • Audit Logging      │
└──────────┬───────────┘
           │
    WireGuard/TLS
           │
┌──────────┴───────────┐
│  Management Console  │
│  (FastAPI + React)   │
│                       │
│  • Engagement Mgmt   │
│  • AI Analysis       │
│  • Approval Workflow │
│  • Report Generation │
└───────────────────────┘
```

---

## 🛠️ Hardware

- **Base**: Raspberry Pi 3 Model B/B+
- **Wireless**: USB WiFi adapter (monitor mode capable)
- **Bluetooth**: USB Bluetooth adapter
- **Physical**: Flipper Zero (UART/USB integration)
- **Power**: Portable power bank or LiPo battery
- **Enclosure**: Compact stealth case

See [`hardware/bill-of-materials.md`](hardware/bill-of-materials.md) for detailed compatibility.

---

## 📚 Software Stack

**Agent (Raspberry Pi)**
- Kali Linux ARM (minimal, <4 GB)
- Python 3.11+ agent service
- Systemd integration
- WireGuard VPN client

**Console (Server/Cloud)**
- Backend: FastAPI (Python)
- Frontend: React + TypeScript
- Database: PostgreSQL
- AI: Ollama (local) or API integration

---

## 📝 Key Features

1. **Authorized-Only Operation**
   - Requires Rules of Engagement (RoE) upload
   - Scope-limited scanning (CIDR allowlists)
   - Immutable audit logging

2. **AI-Assisted Analysis**
   - Reviews findings and proposes next steps
   - **Never executes autonomously**
   - Human approval required for all actions

3. **Comprehensive Reporting**
   - Structured JSON findings
   - Exportable client reports
   - Chain-of-custody audit trails

4. **Flipper Zero Integration**
   - RFID/NFC testing
   - Sub-GHz analysis
   - BadUSB scenarios (authorized only)
   - IR remote testing

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/zebadee2kk/kynee.git
cd kynee

# See documentation for:
# - Hardware setup: docs/build/kali-rpi3-minimal.md
# - Agent installation: agent/README.md
# - Console deployment: console/README.md
```

---

## 📌 Development Roadmap

See [`ROADMAP.md`](ROADMAP.md) for the complete 8-week development plan:

- **Week 1**: Foundations + governance
- **Week 2**: Hardware bring-up + minimal OS
- **Week 3**: Agent v0 (collectors + data model)
- **Week 4**: Secure transport + enrollment
- **Week 5**: Console v0 (backend + UI)
- **Week 6**: AI assistant (human-in-the-loop)
- **Week 7**: Integrations + packaging
- **Week 8**: Beta hardening + documentation

---

## 🤝 Contributing

We welcome contributions from security professionals! Please read:

- [**Contributing Guidelines**](CONTRIBUTING.md)
- [**Code of Conduct**](CODE_OF_CONDUCT.md)
- [**Security Policy**](SECURITY.md)

**Important**: All contributors must acknowledge and agree to our [Ethical Use Policy](ETHICAL_USE_POLICY.md).

---

## 📜 License

Apache License 2.0 — see [LICENSE](LICENSE) for details.

---

## 📧 Contact

- **Security Issues**: See [SECURITY.md](SECURITY.md) for responsible disclosure
- **General Questions**: Open a [GitHub Discussion](https://github.com/zebadee2kk/kynee/discussions)
- **Professional Inquiries**: [Open an issue](https://github.com/zebadee2kk/kynee/issues) with the `business` label

---

## ⚖️ Disclaimer

THIS SOFTWARE IS PROVIDED FOR AUTHORIZED SECURITY TESTING ONLY. Users are solely responsible for ensuring they have proper authorization before deploying this tool. Unauthorized access to computer systems is illegal. The developers assume no liability for misuse.
