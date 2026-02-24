# ADR-0004: Audit Log Immutability Mechanism

## Status
**Accepted** (2026-02-24)

## Context

KYNEĒ audit logs must be **tamper-evident** for legal/compliance purposes. Requirements:

- **Immutability**: Once written, logs cannot be modified or deleted.
- **Integrity**: Tampering must be detectable (even by privileged users).
- **Ordering**: Logs must be time-ordered and linked (no gaps).
- **Performance**: Minimal overhead on agent (Raspberry Pi 3 has limited CPU).
- **Portability**: Must work on local filesystem (no dependency on external blockchain).

**Options Considered**:

1. **Hash Chain (Merkle-like)**
   - Pros: Simple, fast, cryptographically secure, no external deps
   - Cons: Requires sequential writes, reconstruction needed to verify

2. **Append-Only File with Digital Signatures**
   - Pros: Each entry independently signed, non-repudiation
   - Cons: Slower (RSA/ECDSA signing overhead), key management complexity

3. **Write-Once Filesystem (WORM)**
   - Pros: OS-enforced immutability
   - Cons: Not portable, requires special filesystem (e.g., SquashFS), hard to implement on Pi

4. **External Timestamping Service**
   - Pros: Third-party verification, legal validity
   - Cons: Network dependency, cost, latency

5. **Blockchain / Distributed Ledger**
   - Pros: Decentralized, highly tamper-evident
   - Cons: Overkill for single-agent use case, high overhead

## Decision

**Hash chain with periodic remote backup and signature**.

### Architecture

```
Log Entry 1                Log Entry 2                Log Entry 3
┌────────────────┐   ┌────────────────┐   ┌────────────────┐
│ log_id: uuid1    │   │ log_id: uuid2    │   │ log_id: uuid3    │
│ timestamp: ...   │   │ timestamp: ...   │   │ timestamp: ...   │
│ action: ...      │   │ action: ...      │   │ action: ...      │
│ prev_hash: 0000  │   │ prev_hash: H(E1) │   │ prev_hash: H(E2) │
│ signature: S1    │   │ signature: S2    │   │ signature: S3    │
└────────────────┘   └────────────────┘   └────────────────┘
     │                      │                      │
     └───── SHA-256 ──────┘                      │
                              └───── SHA-256 ──────┘
```

### Mechanism

1. **Hash Chain**:
   - Each log entry includes `previous_log_hash` (SHA-256 of previous entry's JSON).
   - First entry has `previous_log_hash: "0000..."` (genesis).
   - Tampering with any entry breaks the chain (subsequent hashes won't match).

2. **HMAC Signature** (Optional):
   - Each entry signed with HMAC-SHA256 using agent's secret key.
   - Prevents forgery even if attacker has filesystem access.
   - Key stored in OS keyring or TPM (if available).

3. **Periodic Transmission**:
   - Agent sends logs to console every 5 minutes (or on disconnect).
   - Console stores immutable copy in PostgreSQL (append-only table).
   - Console verifies hash chain on ingestion.

4. **Verification**:
   - On engagement completion, console exports full chain + signature.
   - Third-party auditor can verify chain integrity offline.

### Rationale

1. **Performance**: SHA-256 is fast (~10ms per entry on Pi 3).
2. **Simplicity**: No external dependencies, pure Python (`hashlib`).
3. **Tamper-Evidence**: Modifying any entry invalidates all subsequent hashes.
4. **Legal Compliance**: Chain + signatures provide non-repudiation (operator cannot deny actions).

## Consequences

### Positive

- **Integrity**: Cryptographically guaranteed tamper-evidence.
- **Portability**: Works offline (no network dependency for local logging).
- **Auditability**: Console has immutable copy for forensics.
- **Performance**: Minimal overhead (~1-2% CPU on Pi 3).

### Negative

- **Sequential Writes**: Must write logs in order (can't parallelize).
- **Recovery**: If chain breaks (e.g., disk corruption), all subsequent entries suspect.
- **Key Management**: HMAC key must be protected (compromise = forgery).

### Neutral

- Not a true blockchain (no consensus, no decentralization), but sufficient for single-agent use case.

## Implementation Details

### Python Example (Agent)

```python
import hashlib
import hmac
import json
from datetime import datetime

class AuditLogger:
    def __init__(self, secret_key: bytes):
        self.secret_key = secret_key
        self.previous_hash = "0" * 64  # Genesis
    
    def log(self, action: dict) -> dict:
        entry = {
            "log_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "previous_log_hash": self.previous_hash,
            **action
        }
        
        # Compute hash (excluding signature field)
        entry_json = json.dumps(entry, sort_keys=True)
        entry_hash = hashlib.sha256(entry_json.encode()).hexdigest()
        
        # Sign entry
        signature = hmac.new(self.secret_key, entry_json.encode(), hashlib.sha256).hexdigest()
        entry["signature"] = signature
        
        # Update chain
        self.previous_hash = entry_hash
        
        # Append to log file
        with open("/var/lib/aetherpi/audit.log", "a") as f:
            f.write(json.dumps(entry) + "\n")
        
        return entry
```

### Verification (Console)

```python
def verify_chain(entries: list[dict], agent_secret_key: bytes) -> bool:
    prev_hash = "0" * 64
    for entry in entries:
        # Recompute hash
        entry_copy = {k: v for k, v in entry.items() if k != "signature"}
        entry_json = json.dumps(entry_copy, sort_keys=True)
        computed_hash = hashlib.sha256(entry_json.encode()).hexdigest()
        
        # Verify signature
        expected_sig = hmac.new(agent_secret_key, entry_json.encode(), hashlib.sha256).hexdigest()
        if entry["signature"] != expected_sig:
            return False  # Forgery detected
        
        # Verify chain
        if entry["previous_log_hash"] != prev_hash:
            return False  # Chain broken
        
        prev_hash = computed_hash
    
    return True
```

## Alternatives Revisited

- **If external timestamping required**: Integrate with [OpenTimestamps](https://opentimestamps.org/) or [RFC 3161](https://tools.ietf.org/html/rfc3161) service.
- **If decentralization needed**: Explore [Trillian](https://github.com/google/trillian) (Certificate Transparency-style log).

---

**Decision Maker**: @zebadee2kk  
**Date**: February 24, 2026  
**Supersedes**: None
