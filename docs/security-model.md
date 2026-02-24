# Security Model

This document explains how KYNEE enforces ethical use and protects sensitive data.

---

## Core Guarantees

- **Authorized use only**: Engagements require a signed RoE.
- **Scope enforcement**: Actions must match approved targets and time windows.
- **Auditability**: Every action is logged, including approvals.
- **Encrypted transport**: Findings and logs are sent over secure channels.

---

## Identity and Authentication

- **Operators** authenticate to the console (JWT with RBAC planned).
- **Agents** enroll with one-time tokens and receive unique device IDs.
- **All actions** link back to an operator or automation context.

---

## Scope Enforcement

The policy engine will block actions outside the engagement scope, including:

- CIDR allowlists
- Hostname allowlists
- Time windows
- Rate limits (max scans per hour)

---

## Audit Logging

Audit logs are designed to be append-only and tamper-evident:

- **Hash chaining**: Each entry includes a hash of the previous entry.
- **Local persistence**: Logs stored on the agent and uploaded to the console.
- **Operator context**: Each action includes who approved it and why.

---

## Secure Transport

- **Primary**: WireGuard VPN between agent and console.
- **Fallback**: HTTPS with mutual authentication (planned).
- **Goal**: Confidentiality and integrity in transit.

---

## AI Guardrails

- AI never executes actions directly.
- Suggestions must cite the RoE or engagement scope.
- Operators must approve or reject each suggestion.

See [docs/ai-assistant.md](ai-assistant.md) for details.

---

## Data Handling

- Evidence should be minimized and redacted when possible.
- Logs and reports are retained per the RoE.
- Sensitive data is encrypted at rest (planned for Week 8 hardening).

---

## Incident Response

If something goes wrong:

1. Stop the activity.
2. Notify the client contact.
3. Preserve logs and evidence.
4. Document the incident in the audit log.

---

## Threats and Mitigations (Summary)

| Threat | Example | Mitigation |
|---|---|---|
| Spoofing | Fake agent device | Enrollment tokens, device identity |
| Tampering | Modified findings | Hash-chained audit logs |
| Repudiation | Denied actions | Operator-linked approvals |
| Information disclosure | Leaked data | Encrypted transport, least data |
| DoS | Over-scanning | Rate limits, scheduling |
| Privilege escalation | Policy bypass | RBAC, scope checks |
