# Rules of Engagement (RoE) Template

**Client**: [Client Organization Name]  
**Engagement ID**: [Unique Identifier]  
**Prepared By**: [Your Company/Team Name]  
**Date**: [Date]  
**Approval Signature**: ______________________  

---

## 1. Authorization

This document authorizes **[Penetration Testing Company]** to conduct security assessment activities against the systems and networks listed in Section 3 (Scope) on behalf of **[Client Organization]**.

**Client Authorizing Official**:
- Name: [Full Name]
- Title: [Position]
- Contact: [Email/Phone]
- Signature: ______________________
- Date: ______________________

---

## 2. Engagement Objectives

### Primary Goals
- [ ] Network vulnerability assessment
- [ ] Wireless security testing (Wi-Fi, Bluetooth)
- [ ] Physical security assessment (RFID, access control)
- [ ] Social engineering testing
- [ ] Web application penetration testing
- [ ] Credential strength and password policy review

### Success Criteria
[Define measurable outcomes, e.g., "Identify all critical/high vulnerabilities on in-scope assets"]

---

## 3. Scope

### In-Scope Assets

**IP Address Ranges**:
```
192.168.1.0/24
10.0.5.0/24
203.0.113.0/29 (public-facing web servers)
```

**Domains/Hostnames**:
```
*.example.com (excluding admin.example.com)
app.client-domain.net
```

**Physical Locations**:
- Main office: [Address]
- Data center: [Address] (badge access required)

**Wireless Networks**:
- SSID: "CorpNet" (2.4/5 GHz)
- SSID: "GuestWiFi"

**Other Systems**:
- RFID badge readers (Building A, floors 1-3)
- VoIP phones (manufacturer: [Vendor])

### Out-of-Scope Assets

**CRITICAL**: The following are **strictly prohibited**:

- Production database servers (`db-prod-01`, `db-prod-02`)
- Payment processing systems (PCI-DSS scope)
- Third-party SaaS platforms (unless explicitly listed)
- IP range: 192.168.100.0/24 (executive office network)
- Physical areas: Executive suite, HR department

---

## 4. Timeline

**Start Date**: [YYYY-MM-DD]  
**End Date**: [YYYY-MM-DD]  

**Testing Windows**:
- Weekdays: 06:00 - 22:00 [Client Timezone]
- Weekends: Prohibited (unless approved)
- Blackout Dates: [e.g., Dec 15-20 (holiday freeze)]

**Milestones**:
- Week 1: External reconnaissance, network scanning
- Week 2: Vulnerability validation, exploitation attempts
- Week 3: Wireless and physical testing
- Week 4: Reporting and remediation consultation

---

## 5. Authorized Testing Methods

### Permitted Techniques
- [x] Network port scanning (TCP/UDP)
- [x] Vulnerability scanning (automated tools)
- [x] Manual exploitation of identified vulnerabilities
- [x] Password guessing (rate-limited to avoid lockouts)
- [x] Wireless sniffing and deauthentication attacks
- [x] RFID/NFC cloning (physical badges)
- [x] Social engineering (phishing emails, pretexting calls)

### Prohibited Techniques
- [ ] Denial of Service (DoS) attacks
- [ ] Data exfiltration beyond proof-of-concept (100 KB limit)
- [ ] Physical destruction of equipment
- [ ] Brute-force attacks on production authentication systems
- [ ] Accessing personal employee data (GDPR/privacy)

### Tool Restrictions
- Metasploit: Allowed (with prior approval for specific exploits)
- SQLMap: Allowed (read-only queries only)
- Responder: Allowed (passive listening mode only)

---

## 6. Communication Plan

### Emergency Contacts

**Client SPOC** (Single Point of Contact):
- Name: [Name]
- Role: [IT Manager / CISO]
- Phone: [24/7 number]
- Email: [secure@client.com]

**Penetration Testing Team Lead**:
- Name: [Your Name]
- Phone: [Your 24/7 number]
- Email: [yourteam@pentestcompany.com]

### Escalation Procedures

**Critical Findings** (e.g., active exploitation, data breach risk):
1. Immediate verbal notification to Client SPOC
2. Follow-up encrypted email within 1 hour
3. Documented in findings tracker

**Service Disruption** (unintended outage):
1. STOP testing immediately
2. Notify Client SPOC via phone
3. Document incident in audit log
4. Joint root-cause analysis within 24 hours

### Status Updates
- Daily: Email summary to Client SPOC
- Weekly: Video call with stakeholders
- Ad-hoc: Slack channel `#pentest-engagement` (if provided)

---

## 7. Data Handling

### Confidentiality
- All findings are **confidential** and covered by NDA (dated [Date])
- Data retention: 90 days post-engagement
- Secure deletion: DoD 5220.22-M (7-pass wipe) or physical destruction

### Evidence Collection
- Screenshots: Redact sensitive data (passwords, PII)
- Packet captures: Encrypted storage (AES-256)
- Credentials: Stored in password manager (1Password / KeePass), not plaintext

### Reporting
- Draft report: Delivered within 5 business days of engagement end
- Final report: Incorporating client feedback, within 10 business days
- Format: PDF (encrypted, password-protected)
- Distribution: Authorized recipients only (listed below)

**Authorized Recipients**:
- [Name], [Title], [Email]
- [Name], [Title], [Email]

---

## 8. Legal and Compliance

### Applicable Laws
- Computer Fraud and Abuse Act (CFAA) — U.S.
- Computer Misuse Act 1990 — UK
- General Data Protection Regulation (GDPR) — EU

### Liability
- **Client** indemnifies testing team for authorized activities within scope
- **Testing team** liable only for gross negligence or willful misconduct
- Insurance: [Testing Company] maintains £1M Cyber Liability coverage

### Regulatory Considerations
- PCI-DSS: Testing follows Requirement 11.3 (penetration testing)
- HIPAA: BAA (Business Associate Agreement) in place (if applicable)
- ISO 27001: Testing aligns with control A.12.6.1 (technical vulnerability management)

---

## 9. Success Criteria and Deliverables

### Deliverables
1. **Executive Summary** (1-2 pages, non-technical)
2. **Technical Report** (detailed findings, CVE references, CVSS scores)
3. **Remediation Roadmap** (prioritized, with timelines)
4. **Evidence Archive** (screenshots, logs, packet captures)
5. **Retest Report** (after 30 days, verify fixes)

### Findings Classification
- **Critical**: Immediate exploitation leading to full system compromise
- **High**: Exploitable with significant impact
- **Medium**: Exploitable with limited impact or requires user interaction
- **Low**: Best-practice violations, no direct exploitability
- **Informational**: Observations, no security impact

---

## 10. Incident Response

### Stop-Work Triggers
- Client requests halt (any reason)
- Unintended service disruption
- Discovery of active threat actor (APT, ransomware)
- Legal/regulatory concern arises

### Joint Investigation
- Testing team provides full audit logs
- Client provides system logs, NetFlow data
- Root-cause analysis documented within 48 hours

---

## 11. Post-Engagement

### Remediation Support
- **Included**: 2 hours of consultation (video calls, email support)
- **Additional**: Available at £150/hour

### Retest
- **Timeline**: 30 days after remediation completion
- **Scope**: Retest only previously identified findings
- **Cost**: 20% of original engagement fee

### Data Destruction
- Client may request early destruction (before 90-day retention)
- Certificate of Destruction provided upon request

---

## 12. Approval and Acceptance

**Client Approval**:

I, **[Client Authorizing Official Name]**, confirm that I have the authority to authorize this security assessment on behalf of **[Client Organization]**. I understand the scope, methods, and risks outlined in this document.

- Signature: ______________________
- Date: ______________________
- Title: ______________________

**Testing Team Acceptance**:

I, **[Penetration Tester Lead Name]**, on behalf of **[Penetration Testing Company]**, accept the terms of this Rules of Engagement and commit to conducting testing within the defined scope and ethical guidelines.

- Signature: ______________________
- Date: ______________________
- License/Certification: [CREST, OSCP, CEH, etc.]

---

## Appendix A: KYNEĒ Device Information

**Device ID**: [Agent UUID from KYNEĒ console]  
**Deployment Location**: [Building/Room]  
**Network Connection**: [Ethernet port #, or "Wi-Fi: SSID"]  
**Power**: [Battery-powered, 8-hour autonomy]  
**Data Exfiltration**: WireGuard VPN to `console.pentestcompany.com:51820`  

**Audit Logging**: All actions logged locally and transmitted to console. Logs include:
- Timestamp (UTC)
- Command executed
- Target IP/MAC address
- Operator ID (who approved the action)
- RoE reference ID

---

**Template Version**: 1.0  
**Last Updated**: February 24, 2026  
**Maintained By**: KYNEĒ Project ([https://github.com/zebadee2kk/kynee](https://github.com/zebadee2kk/kynee))
