# Scope and Authorization Guidelines

## Purpose

This document provides guidance for security professionals using KYNEĒ to ensure all activities are properly authorized, scoped, and documented.

---

## Pre-Engagement Requirements

### 1. Written Authorization

**CRITICAL**: Never deploy KYNEĒ without explicit written permission.

**Required Documents**:
- Signed Rules of Engagement (RoE) — see [template](rules-of-engagement-template.md)
- Non-Disclosure Agreement (NDA)
- Statement of Work (SOW) or contract
- Network diagram with scope highlighted

**Authorizing Officials**:
- Must have legal authority to grant access
- Typically: CIO, CISO, IT Director, or business owner
- For third-party hosting: Additional authorization from service provider

### 2. Scope Definition

**In-Scope Elements** (must be explicitly listed):
- IP address ranges (CIDR notation)
- Domain names and subdomains
- Physical locations (buildings, floors, rooms)
- Wireless networks (SSIDs, BSSIDs)
- Specific systems (hostnames, serial numbers)

**Out-of-Scope Exclusions** (must be clearly documented):
- Production systems with zero-downtime SLAs
- Third-party managed services
- Personal devices (BYOD)
- Sensitive data stores (HR, finance, legal)

**Example Scope Statement**:
```
IN SCOPE:
- 10.0.0.0/8 (internal corporate network)
- *.example.com (excluding admin.example.com)
- Building A, floors 1-3 (physical access testing)
- SSID: "CorpWiFi" (802.11 security testing)

OUT OF SCOPE:
- 10.255.0.0/16 (OT/SCADA network)
- cloud.example.com (AWS-hosted, requires separate authorization)
- Building B (leased space, different legal entity)
```

---

## Engagement Types

### External Penetration Test
- **Perspective**: Internet-facing (attacker outside the network)
- **KYNEĒ Deployment**: Not typical (use from external IP)
- **Authorization**: Client organization only

### Internal Penetration Test
- **Perspective**: Insider threat or post-breach scenario
- **KYNEĒ Deployment**: On client premises, connected to internal network
- **Authorization**: Client + facility security (if applicable)

### Red Team Operation
- **Perspective**: Adversarial simulation (covert)
- **KYNEĒ Deployment**: May involve physical infiltration
- **Authorization**: Client + "white cell" (trusted coordinators)
- **Notifications**: Limited (blue team unaware, but executive sponsor informed)

### Wireless Assessment
- **Perspective**: Wireless-specific vulnerabilities
- **KYNEĒ Deployment**: Positioned for Wi-Fi/Bluetooth range
- **Authorization**: Client + property owner (if testing from parking lot, etc.)

---

## Legal Considerations

### United States
- **Computer Fraud and Abuse Act (CFAA)**: Prohibits unauthorized access
- **Defense**: Written authorization + good faith + no damage
- **Case Law**: *United States v. Morris* (1991), *Pulte Homes v. Laborers* (2011)

### United Kingdom
- **Computer Misuse Act 1990**: Sections 1-3 criminalize unauthorized access
- **Defense**: "Lawful authority" (RoE sufficient if signed by proper authority)
- **Police and Justice Act 2006**: Increased penalties for "reckless" hacking

### European Union
- **GDPR**: Personal data handling during testing
- **Directive 2013/40/EU**: Attacks against information systems
- **Defense**: Legitimate interest + data minimization + client consent

### Australia
- **Criminal Code Act 1995**: Sections 477-478 (cybercrime)
- **Defense**: Authorization + no intent to defraud

### International
- **Council of Europe Convention on Cybercrime**: Harmonized laws across 68+ countries
- **Risk**: Conducting testing from Country A against targets in Country B may violate both jurisdictions

**Best Practice**: Consult legal counsel in every jurisdiction involved.

---

## KYNEĒ Configuration for Compliance

### Scope Enforcement

**CIDR Allowlists** (`agent/config.yaml`):
```yaml
scope:
  allowed_networks:
    - "10.0.0.0/8"
    - "192.168.1.0/24"
  denied_networks:
    - "10.255.0.0/16"  # OT network
```

**Time Windows**:
```yaml
testing_schedule:
  days: ["Mon", "Tue", "Wed", "Thu", "Fri"]
  hours_utc:
    start: "06:00"
    end: "22:00"
  blackout_dates:
    - "2026-12-24"  # Christmas Eve
    - "2026-12-25"  # Christmas Day
```

**Rate Limiting**:
```yaml
rate_limits:
  max_scans_per_hour: 10
  max_packets_per_second: 100
  max_auth_attempts_per_host: 3
```

### Audit Logging

**Required Fields** (every action):
- `timestamp` (ISO 8601, UTC)
- `engagement_id` (links to RoE)
- `operator_id` (who approved the action)
- `action` (e.g., `network_scan`, `wifi_deauth`)
- `target` (IP, MAC, SSID)
- `tool` (e.g., `nmap`, `airodump-ng`)
- `justification` (reason for action)
- `outcome` (success, failure, error)

**Example Log Entry**:
```json
{
  "timestamp": "2026-03-15T14:32:01Z",
  "engagement_id": "ENG-2026-042",
  "operator_id": "alice@pentestco.com",
  "action": "network_scan",
  "target": "10.0.5.0/24",
  "tool": "nmap",
  "command": "nmap -sS -p- -T4 10.0.5.0/24",
  "justification": "Initial reconnaissance per RoE Section 5.1",
  "outcome": "success",
  "findings_count": 42
}
```

---

## Emergency Procedures

### Immediate Stop-Work

If any of the following occur, **STOP ALL TESTING**:

1. **Client requests halt** (any reason, no questions asked)
2. **Service disruption** (unintended outage, performance degradation)
3. **Discovery of active threat** (ransomware, APT, ongoing breach)
4. **Law enforcement contact** (unless client confirms it's expected)
5. **Scope ambiguity** (uncertainty about in-scope vs. out-of-scope)

**Procedure**:
1. Immediately disable KYNEĒ agent (via console "kill switch" or physical power-off)
2. Notify Client SPOC (phone call, not email)
3. Document incident in audit log
4. Preserve all logs and evidence
5. Await client guidance before resuming

### Incident Reporting

**Unintended Impact** (e.g., crashed service):
- Notify client within 15 minutes
- Provide detailed timeline
- Assist with recovery (if requested)
- Document in incident report

**Critical Finding** (e.g., active exploitation by third party):
- Notify client immediately
- Follow client's incident response plan
- Preserve evidence (do not remediate without authorization)
- Coordinate with client's CSIRT/SOC

---

## Post-Engagement Compliance

### Data Retention

**Default Policy** (per KYNEĒ [ETHICAL_USE_POLICY.md](../../ETHICAL_USE_POLICY.md)):
- **90 days** post-engagement
- Secure storage (encrypted, access-controlled)
- Deletion: DoD 5220.22-M or physical destruction
- Certificate of Destruction available upon request

**Client-Requested Early Deletion**:
- Honor within 48 hours
- Provide written confirmation

### Reporting

**Required Sections**:
1. **Executive Summary** (non-technical, business risk focus)
2. **Scope and Methodology** (what was tested, how)
3. **Findings** (structured by severity, with evidence)
4. **Recommendations** (prioritized, actionable)
5. **Appendices** (technical details, screenshots, logs)

**Redaction**:
- Remove or obfuscate PII (names, email addresses)
- Mask full passwords (show first/last character only)
- Sanitize internal IP addresses if report will be shared externally

**Distribution**:
- Only to authorized recipients (listed in RoE)
- Encrypted PDF (AES-256), password via separate channel
- Watermarked "CONFIDENTIAL" on every page

---

## Continuous Compliance

### Periodic Reviews

**Weekly** (during engagement):
- Review audit logs for anomalies
- Confirm all actions within scope
- Update client on progress

**Monthly** (for recurring engagements):
- Re-validate RoE (scope changes?)
- Rotate credentials/keys
- Update threat model

**Annually**:
- Legal counsel review of RoE template
- Insurance policy renewal (cyber liability)
- Staff training on ethics and compliance

### Continuous Training

All operators must complete:
- **Initial**: Ethics and legal compliance training
- **Annual**: Refresher + case studies of legal/ethical failures
- **Certification**: Maintain active OSCP, CEH, CREST, or equivalent

---

## Resources

### Legal References
- [CFAA Text](https://www.law.cornell.edu/uscode/text/18/part-I/chapter-47) (U.S. Code Title 18)
- [Computer Misuse Act 1990](https://www.legislation.gov.uk/ukpga/1990/18/contents) (UK)
- [GDPR Article 6](https://gdpr-info.eu/art-6-gdpr/) (Lawfulness of processing)

### Professional Standards
- [CREST Code of Conduct](https://www.crest-approved.org/membership/code-of-conduct/)
- [PTES Technical Guidelines](http://www.pentest-standard.org/index.php/Main_Page)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)

### Insurance
- [Coalition Cyber Insurance](https://www.coalitioninc.com/) (covers pentesting activities)
- [Hiscox CyberClear](https://www.hiscox.co.uk/cyber-clear) (UK-focused)

---

**Last Updated**: February 24, 2026  
**Maintained By**: KYNEĒ Project Legal Compliance Working Group
