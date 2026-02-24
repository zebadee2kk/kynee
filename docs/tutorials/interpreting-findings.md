# Tutorial: Interpreting KYNEE Findings

This guide explains how to read findings, judge severity, and prioritize remediation.

---

## Anatomy of a Finding

A typical finding includes:

- **Title**: Short summary of the issue
- **Severity**: Critical, High, Medium, Low, Informational
- **Affected assets**: IPs, hosts, domains, or physical locations
- **Evidence**: Scan output, screenshots, packet captures
- **Impact**: What could happen if exploited
- **Recommendation**: How to fix or mitigate

---

## Severity Levels (Quick Guide)

- **Critical**: Immediate compromise or large data loss likely
- **High**: Exploitable with significant impact
- **Medium**: Exploitable but limited impact or complex prerequisites
- **Low**: Best-practice gap with minimal immediate risk
- **Informational**: Observations with no direct security impact

**Tip:** Always align severity with your reporting standard (CVSS, internal policy).

---

## Example: Network Finding

**Title**: SMBv1 Enabled on File Server

- **Severity**: High
- **Assets**: `10.0.5.12`
- **Evidence**: `nmap --script smb-protocols` shows SMBv1
- **Impact**: Known vulnerabilities; weak encryption
- **Recommendation**: Disable SMBv1, enable SMBv2/3

---

## Dealing With False Positives

1. Validate the finding with a second tool or manual check.
2. Confirm the asset is in scope.
3. Update the finding status and add analyst notes.
4. If needed, rescan the target during an approved window.

---

## Prioritizing Remediation

1. **Exploitability**: Can this be exploited with low effort?
2. **Impact**: What would the business lose if this were exploited?
3. **Exposure**: Is the asset internet-facing or internal only?
4. **Compensating controls**: Is there a WAF, MFA, or segmentation?

---

## Reporting Tips

- Use clear, non-technical summaries for executives.
- Include reproducible steps in the technical section.
- Keep evidence minimal but sufficient.
- Avoid sharing sensitive data beyond what is necessary.

---

## Next Steps

- Review the security model: [docs/security-model.md](../security-model.md)
- See the full workflow tutorial: [docs/tutorials/first-engagement.md](first-engagement.md)
