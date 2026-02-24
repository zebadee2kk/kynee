# ADR-0002: Transport Protocol Design

**Status**: Accepted  
**Date**: 2026-02-24  
**Deciders**: @zebadee2kk  
**Consulted**: Network security experts  

---

## Context

The KYNEĒ agent (Raspberry Pi) must communicate securely with the console (server/cloud) to:

- Send heartbeats (device health, status)
- Receive job dispatch commands ("scan 10.0.0.0/24")
- Upload findings and audit logs
- Maintain secure, authenticated, and encrypted channels

**Requirements**:

1. **Encryption**: All data in transit must be encrypted
2. **Authentication**: Mutual authentication (agent ↔ console)
3. **Firewall Traversal**: Works through corporate firewalls (common ports)
4. **Resilience**: Automatic reconnection on network disruption
5. **Auditability**: All communication logged for compliance

**Options Considered**:

### Option 1: WireGuard VPN (Primary)

- ✅ Modern, lightweight VPN protocol
- ✅ Built-in encryption (ChaCha20Poly1305, Curve25519)
- ✅ Low overhead (~4% CPU on Pi 3)
- ✅ Automatic reconnection
- ✅ Simple key management (public/private key pairs)
- ⚠️ UDP port 51820 (may be blocked by restrictive firewalls)
- ⚠️ Requires VPN server on console side

### Option 2: HTTPS (Reverse Tunnel)

- ✅ Works through all firewalls (TCP port 443)
- ✅ TLS 1.3 encryption
- ✅ HTTP/2 for multiplexing
- ✅ Standard web infrastructure
- ⚠️ Higher overhead than WireGuard
- ⚠️ Requires WebSocket or long-polling for bidirectional communication

### Option 3: SSH Reverse Tunnel

- ✅ Ubiquitous, well-understood
- ✅ Strong encryption
- ✅ Works through firewalls (TCP port 22 or 443)
- ⚠️ Higher resource usage
- ⚠️ Requires SSH server on console
- ⚠️ Key management complexity

### Option 4: Custom Protocol (e.g., gRPC over TLS)

- ✅ Optimized for RPC
- ✅ Protocol buffers (efficient serialization)
- ⚠️ Custom implementation effort
- ⚠️ Less auditable than standard protocols

---

## Decision

**We will use a dual-transport strategy:**

1. **Primary**: WireGuard VPN (UDP port 51820)
2. **Fallback**: HTTPS reverse tunnel (TCP port 443)

### Transport Selection Logic

```python
if wireguard_handshake_succeeds():
    use_wireguard()
else:
    log_warning("WireGuard blocked, falling back to HTTPS")
    use_https_reverse_tunnel()
```

### Rationale

1. **WireGuard as Primary**
   - Best performance for authorized penetration testing environments
   - Many clients allow VPN traffic (security testing is expected to use VPNs)
   - Low resource usage on Pi 3
   - Simple key rotation

2. **HTTPS as Fallback**
   - Guarantees connectivity through restrictive firewalls
   - TLS 1.3 provides strong encryption
   - WebSocket or Server-Sent Events (SSE) for console → agent commands
   - Standard HTTP infrastructure (load balancers, reverse proxies)

3. **No SSH Tunnel**
   - Higher resource usage than WireGuard
   - Overlapping functionality with WireGuard
   - Added complexity for key management

---

## Implementation Details

### WireGuard Configuration

**Agent** (`/etc/wireguard/wg0.conf`):
```ini
[Interface]
PrivateKey = <agent-private-key>
Address = 10.200.0.2/24

[Peer]
PublicKey = <console-public-key>
Endpoint = console.example.com:51820
AllowedIPs = 10.200.0.0/24
PersistentKeepalive = 25
```

**Console** (`/etc/wireguard/wg0.conf`):
```ini
[Interface]
PrivateKey = <console-private-key>
Address = 10.200.0.1/24
ListenPort = 51820

[Peer]  # One per agent
PublicKey = <agent-public-key>
AllowedIPs = 10.200.0.2/32
```

**Communication**:
- Agent → Console: HTTP API calls over WireGuard (e.g., `http://10.200.0.1:8000/api/findings`)
- Console → Agent: Not needed (agent polls for jobs)

### HTTPS Fallback

**Agent**:
- Establishes WebSocket connection to `wss://console.example.com:443/agent/ws`
- Sends heartbeats every 30 seconds
- Receives job commands via WebSocket messages

**Console**:
- FastAPI WebSocket endpoint: `/agent/ws`
- TLS 1.3 with certificate pinning (agent trusts specific console cert)

**Message Format**:
```json
{
  "type": "heartbeat",
  "agent_id": "uuid-1234",
  "timestamp": "2026-02-24T20:00:00Z",
  "status": "idle"
}
```

---

## Security Considerations

### Key Management

1. **Enrollment**:
   - Agent generates keypair on first boot
   - Public key sent to console via HTTPS enrollment endpoint (authenticated with one-time token)
   - Console adds agent's public key to WireGuard config
   - Console's public key returned to agent

2. **Key Rotation**:
   - Every 90 days (automated)
   - Agent generates new keypair, uploads new public key
   - Console updates config, signals agent to switch

3. **Key Storage**:
   - Agent: `/etc/wireguard/` (root-only permissions)
   - Console: Database (encrypted at rest)

### TLS Certificate Pinning

- Agent stores console's TLS certificate fingerprint
- Rejects connections if certificate changes (requires manual re-enrollment)
- Mitigates MITM attacks

### Audit Logging

**Every connection event logged**:
```json
{
  "timestamp": "2026-02-24T20:00:00Z",
  "agent_id": "uuid-1234",
  "event": "wireguard_handshake_success",
  "transport": "wireguard",
  "peer_endpoint": "203.0.113.5:51820"
}
```

---

## Consequences

### Positive

- ✅ Works in 99% of environments (WireGuard or HTTPS)
- ✅ Low overhead (WireGuard preferred path)
- ✅ Strong encryption (WireGuard + TLS 1.3)
- ✅ Automatic failover (resilient)
- ✅ Simple key management (no CA needed for WireGuard)

### Negative

- ⚠️ Dual implementation (WireGuard + HTTPS)
- ⚠️ Console must support both transports
- ⚠️ Slightly more complex testing

### Neutral

- WireGuard may require client firewall rules (documented in deployment guide)
- TLS certificate management (Let's Encrypt or self-signed + pinning)

---

## Alternatives Considered and Rejected

### Tor Hidden Service

- ✅ Anonymity, firewall traversal
- ❌ High latency (unusable for real-time scanning)
- ❌ Bandwidth limitations
- ❌ Legal concerns in some jurisdictions

### ZeroTier

- ✅ Mesh VPN, easy setup
- ❌ Third-party dependency (SaaS)
- ❌ Less transparent than WireGuard
- ❌ Not suitable for security-critical infrastructure

---

## Related Decisions

- [ADR-0003: Data Serialization Format](adr-0003-data-serialization.md)
- [ADR-0004: Audit Log Immutability](adr-0004-audit-log-immutability.md)

---

**Last Updated**: February 24, 2026  
**Maintained By**: @zebadee2kk
