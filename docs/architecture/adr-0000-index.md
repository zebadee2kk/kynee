# Architecture Decision Records (ADRs)

## What is an ADR?

An Architecture Decision Record (ADR) is a document that captures an important architectural decision made along with its context and consequences.

**Format**:
- **Title**: Short noun phrase
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Context**: What forces are at play? (technical, political, social, project)
- **Decision**: What did we decide?
- **Consequences**: What becomes easier or harder?

---

## Index of ADRs

| ID | Title | Status | Date |
|----|-------|--------|------|
| [ADR-0001](adr-0001-agent-language.md) | Agent Implementation Language | Accepted | 2026-02-24 |
| [ADR-0002](adr-0002-transport-protocol.md) | Transport Protocol Design | Accepted | 2026-02-24 |
| [ADR-0003](adr-0003-data-serialization.md) | Data Serialization Format | Accepted | 2026-02-24 |
| [ADR-0004](adr-0004-audit-log-immutability.md) | Audit Log Immutability Mechanism | Accepted | 2026-02-24 |
| [ADR-0005](adr-0005-ai-guardrails.md) | AI Recommendation Guardrails | Accepted | 2026-02-24 |

---

## How to Use ADRs

### Creating a New ADR

1. Copy the template from `adr-template.md`
2. Number it sequentially (`adr-NNNN-title.md`)
3. Fill in the sections
4. Submit as a PR with label `architecture`
5. Update this index

### Superseding an ADR

1. Create a new ADR explaining the change
2. Update the old ADR's status to `Superseded by ADR-XXXX`
3. Update this index

---

## Resources

- [ADR GitHub Organization](https://adr.github.io/)
- [Michael Nygard's article](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [ADR Tools](https://github.com/npryce/adr-tools)

---

**Last Updated**: February 24, 2026  
**Maintained By**: @zebadee2kk
