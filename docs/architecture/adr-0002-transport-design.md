# ADR-0002: Transport Protocol Design

**Status**: Proposed  
**Date**: 2026-02-24  
**Deciders**: @zebadee2kk, Architecture Team  
**Technical Story**: Week 4 roadmap milestone

---

## Context

The KYNEĒ agent must communicate securely with the console over untrusted networks. Requirements:

- **Confidentiality**: Findings, credentials, and audit logs must be encrypted
- **Authentication**: Console must verify agent identity (and vice versa)
- **Integrity**: Messages must not be tampered with
- **Firewall Traversal**: Must work through corporate firewalls (outbound-only)
- **Resilience**: Automatic reconnection if connectivity drops
- **Performance**: Low overhead for resource-constrained Pi 3

We need a primary transport mechanism with fallback options.

---

## Decision

**Use WireGuard VPN as primary transport, with HTTPS (port 443) as fallback.**

### Primary: WireGuard

- Layer 3 VPN tunnel (agent <-> console)
- Pre-shared keys + device enrollment
- UDP-based (fast, low overhead)
- Strong cryptography (ChaCha20-Poly1305, Curve25519)
- Peer-to-peer authentication

### Fallback: HTTPS (TLS 1.3)

- Used if WireGuard UDP is blocked
- Reverse tunnel over port 443 (WebSocket or long polling)
- mTLS (mutual TLS) for authentication
- Certificate pinning to prevent MITM

---

## Consequences

### Positive

- **WireGuard**: Excellent performance, minimal CPU overhead, battle-tested
- **Firewall evasion**: HTTPS on 443 bypasses most corporate restrictions
- **Simplicity**: WireGuard is easier to configure than OpenVPN or IPsec
- **Roaming**: WireGuard handles network changes gracefully

### Negative

- **Dual implementation**: Need to maintain both WireGuard and HTTPS paths
- **Complexity**: Automatic fallback detection adds logic
- **Key management**: WireGuard keys must be rotated periodically

### Neutral

- Agent runs WireGuard client (`wg-quick`)
- Console runs WireGuard server (or cloud VPN gateway)
- Enrollment generates unique key pair per agent

---

## Alternatives Considered

### Alternative 1: OpenVPN

**Pros**:
- Mature, widely deployed
- TCP mode for firewall traversal
- Good documentation

**Cons**:
- Higher CPU overhead (TLS handshake)
- More complex configuration
- Slower than WireGuard

**Why Rejected**: WireGuard is faster and simpler for our use case.

### Alternative 2: SSH Reverse Tunnel

**Pros**:
- Built into Linux
- Works over any SSH-capable port
- Easy to set up

**Cons**:
- Not designed for VPN use
- Key management cumbersome
- No roaming support
- Port forwarding fragile

**Why Rejected**: SSH tunnels are brittle for long-lived connections.

### Alternative 3: HTTPS Only (No VPN)

**Pros**:
- Simplest implementation
- No VPN server needed
- Works everywhere

**Cons**:
- Higher latency (HTTP request/response vs. persistent tunnel)
- More complex application-layer protocol
- No IP-level isolation

**Why Rejected**: VPN tunnel simplifies console-to-agent communication (can use any protocol over the tunnel).

---

## Implementation Notes

### WireGuard Setup

**Agent** (`/etc/wireguard/wg0.conf`):
```ini
[Interface]
PrivateKey = <agent-private-key>
Address = 10.8.0.2/24

[Peer]
PublicKey = <console-public-key>
Endpoint = console.example.com:51820
AllowedIPs = 10.8.0.0/24
PersistentKeepalive = 25
```

**Console** (`/etc/wireguard/wg0.conf`):
```ini
[Interface]
PrivateKey = <console-private-key>
Address = 10.8.0.1/24
ListenPort = 51820

[Peer]
PublicKey = <agent-public-key>
AllowedIPs = 10.8.0.2/32
```

### HTTPS Fallback

- Agent polls `https://console.example.com:443/api/v1/jobs` every 30s
- Uploads findings via `POST /api/v1/findings`
- Uses mTLS with client certificate
- WebSocket for real-time communication (if available)

### Automatic Fallback Logic

1. Agent attempts WireGuard connection
2. If no response after 10s, assume UDP blocked
3. Fall back to HTTPS
4. Periodically retry WireGuard (every 5 minutes)

---

## Security Considerations

- **Key rotation**: WireGuard keys rotated every 90 days
- **Certificate pinning**: HTTPS mode pins console certificate
- **Rate limiting**: Console API rate-limits requests (10/min per agent)
- **Replay protection**: WireGuard built-in, HTTPS uses nonces

---

## References

- [WireGuard Protocol](https://www.wireguard.com/protocol/)
- [WireGuard on Raspberry Pi](https://www.pivpn.io/)
- [mTLS Best Practices](https://smallstep.com/hello-mtls/doc/combined/)

---

**Last Updated**: February 24, 2026  
**Status**: Proposed (requires maintainer approval)
