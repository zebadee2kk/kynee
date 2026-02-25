# KYNEĒ Development Roadmap

**Status**: Active Development  
**Start Date**: February 24, 2026  
**Target Beta Release**: April 21, 2026 (Week 8 completion)

---

## Overview

This roadmap outlines an 8-week sprint to deliver a beta-quality KYNEĒ system with all core functionality operational. Each week builds incrementally toward a production-ready portable security assessment platform.

---

## Week 1: Foundations + Governance ✅ COMPLETED
**Dates**: Feb 24 - Mar 2, 2026
**Theme**: Establish project structure, legal framework, and architectural decisions

### Goals
- [x] Repository initialization with governance documents
- [x] Architecture Decision Records (ADRs) for key technical choices
- [x] Define data schemas (findings, inventory, audit logs)
- [x] Legal/compliance documentation templates
- [x] CI/CD pipeline skeleton

### Deliverables
- [x] `README.md`, `LICENSE`, `CODE_OF_CONDUCT.md`, `ETHICAL_USE_POLICY.md`
- [x] `docs/architecture/` — ADRs completed for:
  - [x] Agent implementation language (Python 3.11+)
  - [x] Transport protocol (WireGuard primary, HTTPS fallback)
  - [x] Data serialization format (JSON with JSON Schema validation)
  - [x] Audit log immutability mechanism (hash-chained records)
- [x] `schemas/*.schema.json` — JSON Schema definitions completed:
  - [x] Findings reports (`findings.schema.json`)
  - [x] Asset inventory (`inventory.schema.json`)
  - [x] Audit events (`auditlog.schema.json`)
  - [x] Agent status messages (`agent-status.schema.json`)
- [x] `docs/legal/rules-of-engagement-template.md`
- [x] `.github/workflows/ci.yml` — CI/CD pipelines with linting and security scans
- [x] VS Code workspace configuration for multi-AI development
- [x] Comprehensive project documentation (FAQ, tutorials, dev guides)
- [x] Validation test suites (12 valid + 12 invalid JSON samples)
- [x] Codex AI validation passed (10/10 checks)

### Success Criteria ✅
- [x] Repository structure complete and documented
- [x] Clear technical direction established via ADRs
- [x] RoE template suitable for professional engagements
- [x] All governance documents OSS-compliant
- [x] CI/CD pipeline fully operational

---

## Week 2: Core Modules + Agent Framework ⏳ IN PROGRESS
**Dates**: Mar 3 - Mar 9, 2026
**Theme**: Python core implementation, agent coordination, CLI prototype

### Goals
- [ ] Implement core Python modules from JSON schemas
- [ ] Build agent coordination framework (async/RoE-enforced)
- [ ] Create CLI prototype (4 core commands)
- [ ] Establish test harness (pytest, >80% coverage)

### Deliverables
- [ ] `core/` Python module package:
  - [ ] `core/mission.py` — Mission/engagement data model (from mission-plan-schema.json)
  - [ ] `core/roe.py` — Rules of Engagement validator (from roe-template-schema.json)
  - [ ] `core/findings.py` — Findings container (from findings.schema.json)
  - [ ] `core/inventory.py` — Asset inventory (from inventory.schema.json)
  - [ ] `core/auditlog.py` — Hash-chained audit logging (from auditlog.schema.json)
  - [ ] `core/exceptions.py` — Custom exception hierarchy
- [ ] `agent/` agent framework:
  - [ ] `agent/coordinator.py` — Async agent manager with policy enforcement
  - [ ] `agent/base.py` — Base agent class (abstract)
  - [ ] `agent/policy_engine.py` — RoE policy enforcement
- [ ] `cli/` command-line interface:
  - [ ] `cli/commands.py` — 4 core commands: create, plan, list, status
  - [ ] `cli/main.py` — CLI entry point (Click-based)
- [ ] `tests/unit/` comprehensive unit tests:
  - [ ] Test coverage for all core modules (>80% target)
  - [ ] Test fixtures for mission/RoE/findings
  - [ ] Integration tests for coordinator
- [ ] `docs/api/` API reference
- [ ] `requirements.txt` with production + dev dependencies

### Success Criteria
- [ ] All 5 core modules pass unit tests (>80% coverage)
- [ ] Agent coordinator successfully manages 2+ mock agents
- [ ] CLI executes 4 commands without errors
- [ ] Audit logs hash-chain validation works end-to-end
- [ ] CI/CD pipeline green (all tests passing)

---

## Week 3: Agent v0 (Data Model + Local Collectors)
**Dates**: Mar 10 - Mar 16, 2026  
**Theme**: Agent core functionality and collection plugins

### Goals
- [ ] Agent skeleton as systemd service
- [ ] Configuration management (YAML/TOML)
- [ ] Device identity and enrollment flow
- [ ] Collection adapters (network, Wi-Fi, Bluetooth)
- [ ] Structured JSON output per schemas

### Deliverables
- [ ] `agent/aetherpi_agent/`:
  - `config.py` — Configuration loader
  - `identity.py` — Device UUID, enrollment tokens
  - `scheduler.py` — Job runner (APScheduler)
  - `collectors/network.py` — Nmap wrapper
  - `collectors/wireless.py` — Airodump-ng wrapper
  - `collectors/bluetooth.py` — Hcitool/bluetoothctl wrapper
  - `parsers/` — Output parsers to JSON
  - `auditlog/writer.py` — Local append-only log
- [ ] `agent/packaging/systemd/aetherpi-agent.service`
- [ ] `agent/tests/` — Unit tests for collectors
- [ ] `agent/README.md` — Installation and usage

### Success Criteria
- Agent starts via systemd, runs scheduled scans
- Outputs valid JSON matching `schemas/findings.schema.json`
- All actions logged to `/var/lib/aetherpi/audit.log`

---

## Week 4: Secure Transport + Device Enrollment
**Dates**: Mar 17 - Mar 23, 2026  
**Theme**: Encrypted communications and policy enforcement

### Goals
- [ ] WireGuard VPN tunnel setup (agent ↔ console)
- [ ] Device enrollment (one-time pairing, key exchange)
- [ ] Message protocol (heartbeats, job dispatch, results upload)
- [ ] Policy engine (scope constraints, rate limits)

### Deliverables
- [ ] `infra/wireguard/` — Server/client config templates
- [ ] `agent/aetherpi_agent/transport/`:
  - `wireguard.py` — VPN management
  - `protocol.py` — Message framing (protobuf or JSON+signatures)
  - `client.py` — Console API client (HTTPS fallback)
- [ ] `agent/aetherpi_agent/policy/engine.py` — Scope enforcement:
  - CIDR allowlist validation
  - Time window checks
  - Rate limiting (max scans/hour)
- [ ] `docs/architecture/comms-design.md` — Protocol spec
- [ ] `scripts/provisioning/enroll-device.sh` — Enrollment helper

### Success Criteria
- Agent successfully connects to console via WireGuard
- Enrollment generates unique device ID and keys
- Policy engine blocks out-of-scope scan attempts

---

## Week 5: Console v0 (Backend + Basic UI)
**Dates**: Mar 24 - Mar 30, 2026  
**Theme**: Management console with engagement workflow

### Goals
- [ ] Backend API (FastAPI): auth, engagements, assets, findings
- [ ] Frontend (React): device list, engagement creation, results viewer
- [ ] Database schema (PostgreSQL)
- [ ] Basic reporting (Markdown export)

### Deliverables
- [ ] `console/backend/app/`:
  - `main.py` — FastAPI app
  - `auth/` — JWT authentication, RBAC
  - `api/` — REST endpoints:
    - `/devices` — List, enroll, manage agents
    - `/engagements` — Create, configure scope
    - `/findings` — Ingest, query, filter
    - `/audit` — View immutable logs
  - `services/` — Business logic
  - `storage/` — Database models (SQLAlchemy)
- [ ] `console/backend/migrations/` — Alembic database migrations
- [ ] `console/frontend/src/`:
  - Device dashboard
  - Engagement creation wizard (RoE upload, scope entry)
  - Findings table (filterable, sortable)
  - Audit log viewer
- [ ] `docs/api/openapi.yaml` — API specification
- [ ] `docker-compose.yml` — Console + PostgreSQL

### Success Criteria
- Console UI accessible at `https://localhost:8443`
- Can create engagement, upload RoE, define scope
- Findings from agents display in real-time

---

## Week 6: AI Assistant (Human-in-the-Loop)
**Dates**: Mar 31 - Apr 6, 2026  
**Theme**: AI analysis and recommendation engine

### Goals
- [ ] AI worker that analyzes findings and suggests next steps
- [ ] Prompt templates with ethical guardrails
- [ ] Approval workflow (operators accept/reject suggestions)
- [ ] Integration with Ollama (local) or OpenAI API

### Deliverables
- [ ] `console/backend/app/ai/`:
  - `analyzer.py` — Findings ingestion, context preparation
  - `prompts.py` — Template library:
    - "Analyze these findings and suggest authorized next steps"
    - "Propose credential-testing strategies within scope"
    - Guardrails: refuse out-of-scope, require RoE citation
  - `recommender.py` — Generate action proposals (JSON)
  - `ollama_client.py` / `openai_client.py` — LLM integrations
- [ ] `console/frontend/src/`:
  - AI suggestions panel
  - Approval queue (approve, reject, modify)
  - Reason code selector (maps to audit/compliance narrative)
- [ ] `docs/architecture/ai-design.md` — Prompt engineering guide

### Success Criteria
- AI generates 3-5 actionable suggestions per finding set
- All suggestions require explicit operator approval
- Approved actions logged with reason codes and operator ID

---

## Week 7: Integrations + Packaging
**Dates**: Apr 7 - Apr 13, 2026  
**Theme**: Flipper Zero, release artifacts, end-to-end testing

### Goals
- [ ] Flipper Zero control module (RFID, sub-GHz, IR)
- [ ] Agent packaging (.deb, tarball)
- [ ] Console Docker images
- [ ] CI/CD release pipeline with SBOM
- [ ] End-to-end test harness

### Deliverables
- [ ] `agent/aetherpi_agent/collectors/flipper.py`:
  - Serial/USB communication (pyserial)
  - Commands: RFID read, sub-GHz scan, IR capture
  - Explicit per-engagement enablement flag
  - Enhanced audit logging for physical-layer actions
- [ ] `hardware/flipper/integration-notes.md`
- [ ] `agent/packaging/deb/` — Debian package build
- [ ] `console/backend/Dockerfile`, `console/frontend/Dockerfile`
- [ ] `.github/workflows/release.yml` — Automated releases:
  - Version tagging
  - Artifact uploads (GitHub Releases)
  - SBOM generation (SPDX format)
- [ ] `scripts/e2e-test.sh` — Full workflow:
  1. Start console
  2. Enroll simulated agent
  3. Create engagement
  4. Inject canned findings
  5. Trigger AI analysis
  6. Approve action
  7. Verify audit log

### Success Criteria
- Flipper integration works on test hardware
- Agent installs via `.deb` package
- Console deploys with `docker-compose up`
- E2E test passes on CI

---

## Week 8: Beta Hardening + Documentation
**Dates**: Apr 14 - Apr 21, 2026  
**Theme**: Security review, usability polish, public beta release

### Goals
- [ ] Threat model review and mitigation backlog
- [ ] Usability testing with professional operators
- [ ] Comprehensive documentation
- [ ] Beta (v0.9) release

### Deliverables
- [ ] `docs/architecture/threat-model.md` — STRIDE analysis:
  - Spoofing: Device identity, console auth
  - Tampering: Audit logs, findings integrity
  - Repudiation: Non-repudiable logging
  - Information disclosure: Credential exposure, network sniffing
  - Denial of service: Rate limiting, resource exhaustion
  - Elevation of privilege: Policy bypass, AI jailbreak
- [ ] Mitigation implementations:
  - [ ] Secrets storage (encrypted, OS keyring)
  - [ ] Update signing (GPG/cosign)
  - [ ] Tamper evidence (hash-chained audit logs)
- [ ] `docs/ops/deployment-guide.md` — Production deployment:
  - Server sizing (CPU, RAM, disk)
  - Network architecture (VPN, firewall rules)
  - Backup strategy
- [ ] `docs/ops/incident-response.md` — Compromise runbooks
- [ ] Usability improvements:
  - Engagement templates (common scenarios)
  - Default scope presets (RFC1918 private ranges)
  - One-click report export
- [ ] **v0.9 Beta Release**:
  - [ ] Release notes
  - [ ] Installation guide
  - [ ] Demo walkthrough video
  - [ ] Compliance checklist (PDF)

### Success Criteria
- Threat model reviewed by 2+ security professionals
- Beta testers complete test engagement end-to-end
- Documentation sufficient for independent deployment
- Public release tagged and announced

---

## Post-Beta (Weeks 9-12)

### Community Feedback Phase
- [ ] Bug triage and hotfixes
- [ ] Feature requests prioritization
- [ ] Security audit (third-party if budget allows)
- [ ] Performance optimization (large-scale scans)

### Path to v1.0
- [ ] Advanced reporting (PDF, charts, executive summaries)
- [ ] Multi-user RBAC (admin, operator, analyst roles)
- [ ] Plugin system for custom collectors
- [ ] Cloud deployment (AWS/GCP Terraform modules)
- [ ] Mobile app for console (read-only)

---

## Success Metrics

**Technical**:
- Agent uptime: >99% during 24-hour engagements
- Findings schema compliance: 100%
- Audit log integrity: No gaps or tampering
- AI suggestion relevance: >70% approval rate

**Community**:
- 10+ professional beta testers
- 3+ hardware compatibility confirmations
- 5+ documentation PRs from external contributors

**Legal**:
- Zero reports of unauthorized use
- RoE template used in 5+ real engagements
- Legal review by cybersecurity firm counsel

---

## Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Hardware unavailability (Pi 3 shortages) | High | Document Pi 4/Zero 2W alternatives |
| WireGuard firewall blocking | Medium | Implement HTTPS fallback (443/tcp) |
| AI hallucinations (bad suggestions) | High | Strict guardrails, human approval mandatory |
| Licensing challenges (Kali tools) | Medium | Legal review, clear GPL compliance |
| Misuse by bad actors | Critical | Ethical Use Policy, community reporting, no autonomous features |

---

## Communication Plan

- **Weekly Updates**: GitHub Discussions ("Week X Progress" threads)
- **Milestones**: Tag releases (`v0.1-week3`, `v0.5-week5`, etc.)
- **Demos**: YouTube videos at weeks 4, 6, 8
- **Community Calls**: Bi-weekly (Fridays, 1500 UTC) via Discord/Zoom

---

**Last Updated**: February 24, 2026  
**Maintainer**: @zebadee2kk
