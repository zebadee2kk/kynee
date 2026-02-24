# ADR-0002: Secure Transport Design

## Status
**Accepted** (2026-02-24)

## Context

The KYNEĒ agent must communicate securely with the console from potentially hostile networks during penetration tests. Requirements:

- **Confidentiality**: Findings, credentials, and audit logs must be encrypted in transit.
- **Integrity**: Data must not be tampered with.
- **Authentication**: Console must verify agent identity; agent must verify console.
- **Firewall Evasion**: Many corporate networks block non-HTTP(S) traffic.
- **Reliability**: Connection must auto-recover from network interruptions.

**Options Considered**:

1. **WireGuard VPN**
   - Pros: Modern, fast, minimal config, built into Linux kernel 5.6+, UDP-based
   - Cons: UDP may be blocked by strict firewalls

2. **HTTPS (TLS 1.3) with mTLS**
   - Pros: TCP/443 is rarely blocked, well-understood, good library support
   - Cons: More overhead than WireGuard, requires X.509 cert management

3. **SSH Reverse Tunnel**
   - Pros: Ubiquitous, TCP-based, can tunnel over 443
   - Cons: Legacy protocol, slower than modern alternatives, complex key management

4. **Tor Hidden Service**
   - Pros: Anonymity, NAT traversal
   - Cons: Slow, unreliable, may raise suspicion in corporate environments

## Decision

**Primary**: WireGuard VPN (UDP/51820)  
**Fallback**: HTTPS (TLS 1.3) over TCP/443 with mTLS

### Architecture

```
Agent (Pi 3)                    Console (Server)
│                                │
├─ WireGuard client            │
│  (wg0: 10.200.0.x/24)         ├─ WireGuard server
│                                │  (wg0: 10.200.0.1/24)
│  Attempt connection...        │
│  │                           │
│  ├─ Success? → Use WireGuard  │
│  │                           │
│  └─ Timeout? → Fallback      │
│                                │
├─ HTTPS client (mTLS)        ├─ HTTPS server (nginx)
│  POST /api/v1/agent/status   │  (TLS 1.3 + client cert)
│  POST /api/v1/findings       │
```

### Rationale

1. **WireGuard Primary**:
   - Fastest option (minimal cryptographic overhead).
   - Kernel-level implementation (no userspace daemon).
   - Simple config (public/private key pairs, no PKI).
   - Auto-reconnect via `PersistentKeepalive`.

2. **HTTPS Fallback**:
   - TCP/443 is universally allowed (even in restrictive environments).
   - mTLS ensures mutual authentication (agent cert + console cert).
   - Can use Let's Encrypt for console cert (agent cert self-signed).

3. **Enrollment Flow**:
   - Agent generates WireGuard keypair on first boot.
   - Enrollment API (HTTPS) exchanges keys: agent sends public key, console returns server public key + assigned IP.
   - Agent configures WireGuard, tests connection.
   - If WireGuard fails (firewall blocks UDP/51820), agent falls back to HTTPS for all communication.

## Consequences

### Positive

- **Performance**: WireGuard is 2-3x faster than OpenVPN/IPsec.
- **Reliability**: Fallback ensures connectivity even in restrictive networks.
- **Security**: Both options provide strong encryption (ChaCha20-Poly1305 for WireGuard, AES-256-GCM for TLS 1.3).
- **Simplicity**: WireGuard config is ~10 lines vs. 100+ for OpenVPN.

### Negative

- **Dual Implementation**: Must maintain two transport paths (increases code complexity).
- **Firewall Detection**: Fallback requires timeout detection (adds ~10s latency on first connect if WireGuard is blocked).
- **mTLS Overhead**: Certificate management (issuance, rotation, revocation) for HTTPS path.

### Neutral

- WireGuard is relatively new (2020), but widely adopted and audited.
- HTTPS fallback means we can't rely on WireGuard-only features (e.g., roaming IP).

## Implementation Details

### WireGuard Config (Agent)

```ini
[Interface]
PrivateKey = <agent_private_key>
Address = 10.200.0.x/24
DNS = 10.200.0.1

[Peer]
PublicKey = <console_public_key>
AllowedIPs = 10.200.0.0/24
Endpoint = console.pentestco.com:51820
PersistentKeepalive = 25
```

### Fallback Logic (Python)

```python
import socket
import time

def test_wireguard():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        sock.connect(("10.200.0.1", 8000))  # Console API over WireGuard
        sock.close()
        return True
    except (socket.timeout, socket.error):
        return False

if test_wireguard():
    transport = "wireguard"
else:
    transport = "https"  # Fallback
```

## Alternatives Revisited

- **If WireGuard adoption issues**: Switch to HTTPS-only (simplifies, but loses performance).
- **If extreme firewall evasion needed**: Implement domain fronting or tunneling over DNS (future consideration).

---

**Decision Maker**: @zebadee2kk  
**Date**: February 24, 2026  
**Supersedes**: None
