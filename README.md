# KYNEĒ

**AI-Assisted Security Assessment Platform**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Active_Development-blue.svg)](ROADMAP.md)

> Named after the Helm of Hades — the mythological device that granted invisibility. Built for security professionals who need to see everything, quietly.

---

## The Problem

Penetration testing is time-consuming, expensive, and inconsistent. Most organisations either can't afford it regularly, or rely on point-in-time assessments that are outdated before the report lands.

At the same time, AI is transforming what's possible in security tooling — but most teams don't have the infrastructure to operationalise it safely or at scale.

---

## What KYNEĒ Does

KYNEĒ is a portable, AI-assisted penetration testing platform built for **authorised security assessments**. It combines lightweight hardware with intelligent automation to deliver consistent, documented, repeatable security testing.

Key capabilities:

- **Autonomous network discovery** — intelligent scanning with prioritised target analysis
- **Wireless and Bluetooth reconnaissance** — WPA/WPA2, BLE device enumeration
- **AI-powered recommendations** — LLM-driven next-step suggestions based on findings
- **Rules of Engagement enforcement** — automated scope validation; it won't act outside authorised boundaries
- **Immutable audit logging** — hash-chained, cryptographically verified records of every action
- **Secure web console** — engagement management and real-time reporting

---

## Designed for Authorised Use Only

KYNEĒ is built exclusively for **authorised penetration testing** with written permission from the asset owner. Every engagement requires a Rules of Engagement file. Scope is enforced programmatically — the agent cannot act outside defined boundaries.

Unauthorised use is illegal. See [Ethical Use Policy](ETHICAL_USE_POLICY.md).

---

## Who It's For

- Security teams running internal assessments on authorised infrastructure
- Fractional CISOs and security consultants conducting client engagements
- IT leaders who need repeatable, documented evidence of security posture
- Organisations moving beyond checkbox compliance toward continuous assurance

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Agent Platform | Raspberry Pi (ARM), Python 3.11+ |
| AI Integration | Local LLM + cloud model routing |
| Policy Engine | Custom RoE enforcement framework |
| Audit Logging | Hash-chained append-only logs |
| Transport | WireGuard (encrypted comms) |
| Console | FastAPI backend, React frontend |
| Testing | 74 unit tests, 81.98% coverage |

---

## Status

Active development. Core infrastructure, policy engine, and audit framework are complete with 81.98% test coverage. Network collectors and secure console are in build.

See [ROADMAP.md](ROADMAP.md) for the full delivery timeline.

---

## About

KYNEĒ is built and maintained by [Richard Ham](https://richardham.co.uk) — Fractional IT & Security Leader with 25 years of enterprise IT experience. It was designed to make professional-grade security assessment accessible, consistent, and fully auditable.

---

## Security

To report a vulnerability, please use GitHub Security Advisories rather than opening a public issue. See [SECURITY.md](SECURITY.md).

## License

Apache License 2.0 — see [LICENSE](LICENSE)
