# ADR-0004: Audit Log Immutability Mechanism

**Status**: Proposed  
**Date**: 2026-02-24  
**Deciders**: @zebadee2kk, Architecture Team  
**Technical Story**: Week 3 roadmap milestone

---

## Context

KYNEĒ requires tamper-evident audit logging for compliance and legal defensibility. Every agent action must be logged immutably with:

- **Integrity**: Logs cannot be modified after creation
- **Non-repudiation**: Operators cannot deny actions they authorized
- **Chain of custody**: Logs form a verifiable sequence
- **Forensic value**: Logs suitable for incident response and court evidence

We need a mechanism to ensure audit logs are immutable and tamper-evident.

---

## Decision

**Use cryptographic hash chaining (blockchain-style) with optional remote attestation.**

### Mechanism

Each audit log entry includes:

1. **`log_hash`**: SHA-256 hash of this entry's content
2. **`previous_log_hash`**: SHA-256 hash of the previous entry

This creates an append-only chain where tampering with any entry breaks the chain.

### Formula

```
log_hash = SHA256(log_id || timestamp || engagement_id || action || ... || previous_log_hash)
```

### Storage

- **Local**: Append-only file `/var/lib/aetherpi/audit.log` (immutable via `chattr +a`)
- **Remote**: Periodic upload to console (every 5 minutes or on-demand)
- **Backup**: Optional write to write-once storage (S3 Object Lock, WORM drive)

---

## Consequences

### Positive

- **Tamper detection**: Any modification breaks the hash chain
- **Simple implementation**: No external dependencies (just SHA-256)
- **Verifiable**: Anyone can verify chain integrity
- **Legal defensibility**: Cryptographic proof of log integrity

### Negative

- **No deletion**: Logs cannot be deleted (GDPR compliance requires careful design)
- **Chain break on corruption**: If one entry is lost, chain breaks (mitigated by remote backup)
- **Not a distributed ledger**: Single point of failure (agent storage)

### Neutral

- Hash chain verified on console ingestion
- Broken chains trigger alerts
- Logs can be exported for external verification

---

## Alternatives Considered

### Alternative 1: Database Append-Only Table

**Pros**:
- Leverage database ACID guarantees
- Easy to query

**Cons**:
- Database can still be modified by admin
- No cryptographic proof of integrity
- Requires database on agent (resource overhead)

**Why Rejected**: No tamper-evidence without hash chaining.

### Alternative 2: External Blockchain (Ethereum, Hyperledger)

**Pros**:
- Truly distributed, immutable
- Third-party verification

**Cons**:
- Requires internet connectivity (not guaranteed)
- Transaction costs (Ethereum gas fees)
- Overkill for single-tenant use case
- Privacy concerns (public blockchain)

**Why Rejected**: Complexity and cost not justified; hash chain provides sufficient integrity.

### Alternative 3: TPM (Trusted Platform Module) Sealing

**Pros**:
- Hardware-backed integrity
- Tamper-resistant

**Cons**:
- Raspberry Pi 3 lacks TPM
- Requires TPM 2.0 hardware module (additional cost)
- Complex key management

**Why Rejected**: Hardware not available on target platform; future enhancement for enterprise deployments.

### Alternative 4: Centralized Syslog (rsyslog, Splunk)

**Pros**:
- Real-time remote logging
- Centralized visibility

**Cons**:
- No cryptographic integrity
- Relies on network availability
- Not immutable (syslog server can delete logs)

**Why Rejected**: Useful as supplement, but not sufficient for immutability.

---

## Implementation Notes

### Agent Log Writer (Python)

```python
import hashlib
import json
from datetime import datetime, timezone

class AuditLogger:
    def __init__(self, log_file='/var/lib/aetherpi/audit.log'):
        self.log_file = log_file
        self.previous_hash = self._get_last_hash()
    
    def log(self, entry: dict):
        entry['timestamp'] = datetime.now(timezone.utc).isoformat()
        entry['previous_log_hash'] = self.previous_hash
        
        # Compute hash
        entry_str = json.dumps(entry, sort_keys=True)
        entry['log_hash'] = hashlib.sha256(entry_str.encode()).hexdigest()
        
        # Append to file
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(entry) + '\n')
        
        # Update chain
        self.previous_hash = entry['log_hash']
    
    def _get_last_hash(self):
        # Read last line from log file
        try:
            with open(self.log_file, 'r') as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1])
                    return last_entry['log_hash']
        except FileNotFoundError:
            pass
        return '0' * 64  # Genesis hash
```

### Verification (Console)

```python
def verify_audit_log(log_entries: list) -> bool:
    previous_hash = '0' * 64  # Genesis
    
    for entry in log_entries:
        # Recompute hash
        entry_copy = {k: v for k, v in entry.items() if k != 'log_hash'}
        entry_str = json.dumps(entry_copy, sort_keys=True)
        computed_hash = hashlib.sha256(entry_str.encode()).hexdigest()
        
        # Verify hash
        if computed_hash != entry['log_hash']:
            return False  # Entry tampered
        
        # Verify chain
        if entry['previous_log_hash'] != previous_hash:
            return False  # Chain broken
        
        previous_hash = entry['log_hash']
    
    return True  # All good
```

### File System Protection

Make log file append-only on Linux:

```bash
sudo chattr +a /var/lib/aetherpi/audit.log
```

This prevents deletion or modification, only appends allowed (even by root).

---

## GDPR Considerations

Audit logs may contain personal data (operator IDs, IP addresses). To comply with GDPR:

- **Pseudonymization**: Hash operator IDs (one-way function)
- **Retention limits**: Delete logs after engagement + 90 days (per ETHICAL_USE_POLICY.md)
- **Right to erasure**: For non-audit data only (audit logs exempt under legal obligation)
- **Data minimization**: Log only necessary fields

GDPR Article 17(3)(b) exempts data processed "for compliance with a legal obligation" (audit trails for legal defense).

---

## References

- [Merkle Trees and Hash Chains](https://en.wikipedia.org/wiki/Merkle_tree)
- [Linux chattr](https://man7.org/linux/man-pages/man1/chattr.1.html)
- [GDPR Article 17 (Right to erasure)](https://gdpr-info.eu/art-17-gdpr/)
- [NIST SP 800-92: Guide to Computer Security Log Management](https://csrc.nist.gov/publications/detail/sp/800-92/final)

---

**Last Updated**: February 24, 2026  
**Status**: Proposed (requires maintainer approval)
