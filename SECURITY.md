# Security Policy

## Supported Versions

We release security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 0.x     | :white_check_mark: |

Once version 1.0 is released, we will support the latest minor version and provide critical patches for the previous minor version.

---

## Reporting a Vulnerability

**DO NOT open public GitHub issues for security vulnerabilities.**

### Responsible Disclosure Process

1. **Report Privately**
   - Email: **security@[project-domain]** (to be established)
   - Or use [GitHub Security Advisories](https://github.com/zebadee2kk/kynee/security/advisories/new)

2. **Include in Your Report**
   - Description of the vulnerability
   - Steps to reproduce (proof-of-concept)
   - Potential impact assessment
   - Affected versions
   - Your contact information (for follow-up)

3. **What to Expect**
   - **Acknowledgment**: Within 48 hours
   - **Initial Assessment**: Within 7 days
   - **Status Updates**: Every 14 days until resolution
   - **Coordinated Disclosure**: We'll work with you on timing

4. **Timeline**
   - **Critical vulnerabilities**: Patch within 7 days
   - **High severity**: Patch within 30 days
   - **Medium/Low severity**: Patch in next scheduled release

---

## Scope

### In Scope

- **Agent security**: Privilege escalation, credential exposure, command injection
- **Console security**: Authentication bypass, SQL injection, XSS, CSRF
- **Transport security**: Cryptographic weaknesses, MITM vulnerabilities
- **AI module**: Prompt injection leading to unauthorized actions
- **Audit logging**: Log tampering, chain-of-custody bypass
- **Policy enforcement**: Scope constraint bypass, authorization failures

### Out of Scope

- Social engineering attacks against users
- Denial of Service (DoS) against authorized deployments
- Physical attacks on hardware
- Misuse of the tool for unauthorized access (see [ETHICAL_USE_POLICY.md](ETHICAL_USE_POLICY.md))

---

## Security Best Practices for Users

1. **Keep software updated**: Run latest stable version
2. **Secure RoE documents**: Encrypt and access-control authorization files
3. **Rotate credentials**: Change WireGuard keys and console passwords regularly
4. **Monitor audit logs**: Review for suspicious activity
5. **Encrypt at rest**: Use full-disk encryption on Raspberry Pi SD cards
6. **Segment networks**: Isolate KYNEĒ console from production infrastructure

---

## Security Hardening Checklist

See [`docs/build/hardening-baseline.md`](docs/build/hardening-baseline.md) for comprehensive guidance:

- [ ] Minimal OS surface (unnecessary services disabled)
- [ ] Host-based firewall (iptables/nftables)
- [ ] Mandatory Access Control (SELinux/AppArmor)
- [ ] Encrypted communications (WireGuard + TLS 1.3)
- [ ] Secure boot (if hardware supports)
- [ ] Immutable audit logs (append-only storage)
- [ ] Rate limiting on API endpoints
- [ ] Multi-factor authentication for console

---

## Vulnerability Disclosure Credit

We maintain a [Security Hall of Fame](docs/security-hall-of-fame.md) to recognize researchers who responsibly disclose vulnerabilities. With your permission, we will:

- Credit you in release notes
- List your name/handle in our Hall of Fame
- Link to your preferred profile (GitHub, website, etc.)

You may choose to remain anonymous.

---

## Security Development Lifecycle

All code changes undergo:

1. **Static Analysis**: Automated security scanning (CodeQL, Bandit)
2. **Dependency Scanning**: Regular CVE checks (Dependabot)
3. **Code Review**: Security-focused peer review for sensitive modules
4. **Testing**: Security test suite (authentication, authorization, injection)

See [`.github/workflows/security-scan.yml`](.github/workflows/security-scan.yml) for CI/CD security gates.

---

## Cryptography

KYNEĒ uses industry-standard cryptography:

- **Transport**: WireGuard (Noise protocol), TLS 1.3
- **At-rest**: AES-256-GCM (for sensitive configuration)
- **Hashing**: SHA-256 (audit log chains), Argon2id (password storage)
- **Random**: OS-provided CSPRNG (e.g., `/dev/urandom`, `secrets` module)

**We do not implement custom cryptography.**

---

## Third-Party Dependencies

We audit dependencies quarterly and maintain a Software Bill of Materials (SBOM):

- Automated: `Dependabot` for CVE alerts
- Manual: Review of transitive dependencies for supply chain risks
- Pinning: Lock files ensure reproducible builds

See [`third_party/licenses/`](third_party/licenses/) for attribution.

---

## Incident Response

If KYNEĒ is compromised in a production engagement:

1. **Isolate**: Disconnect affected agents from network
2. **Preserve**: Capture memory dumps, logs, and disk images
3. **Notify**: Inform client per RoE incident response plan
4. **Analyze**: Determine root cause and scope
5. **Remediate**: Patch vulnerability, rotate credentials
6. **Report**: Document findings and lessons learned

See [`docs/ops/incident-response.md`](docs/ops/incident-response.md) for detailed runbooks.

---

## Contact

- **Security Team**: security@[project-domain]
- **PGP Key**: [To be published]
- **GitHub Security Advisories**: [https://github.com/zebadee2kk/kynee/security/advisories](https://github.com/zebadee2kk/kynee/security/advisories)

---

**Last Updated**: February 24, 2026
