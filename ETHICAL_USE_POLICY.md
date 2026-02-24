# Ethical Use Policy

## Purpose

KYNEĒ is designed exclusively for **authorized security assessments** conducted by licensed professionals. This policy establishes clear boundaries for legal and ethical use.

---

## ✅ Authorized Use

You may use KYNEĒ if you meet **ALL** of these conditions:

1. **Professional Authorization**
   - You are a licensed penetration tester, security researcher, or red team operator
   - You are employed by or contracted to a legitimate cybersecurity firm
   - You are testing your own infrastructure

2. **Written Permission**
   - You have explicit, documented authorization from the asset owner
   - A signed Rules of Engagement (RoE) document exists
   - The scope, timeline, and methods are clearly defined

3. **Legal Compliance**
   - Your activities comply with all applicable laws in your jurisdiction
   - You have consulted legal counsel if uncertain
   - You understand penalties for unauthorized access

4. **Human Oversight**
   - All AI-suggested actions require human approval
   - No autonomous exploitation or destructive actions
   - Operators remain accountable for all system behavior

---

## ❌ Prohibited Use

You **MUST NOT** use KYNEĒ for:

- Unauthorized network scanning or access
- Malicious hacking, data theft, or sabotage
- Bypassing security controls without permission
- Personal gain through illegal access
- Activities violating local, national, or international law
- Credential stuffing, DDoS, or other attacks
- Testing third-party systems without written consent

---

## 🛡️ Safety Guardrails

KYNEĒ includes technical controls to enforce ethical use:

1. **Scope Enforcement**
   - CIDR allowlists prevent out-of-scope scanning
   - Time-window restrictions limit engagement duration
   - Rate limiting prevents service disruption

2. **Audit Logging**
   - Immutable logs of all actions
   - Chain-of-custody tracking
   - Tamper-evident event recording

3. **AI Restrictions**
   - Analysis-only mode (no autonomous execution)
   - Requires explicit operator approval for all suggested actions
   - Refuses out-of-scope recommendations

4. **Mandatory RoE Upload**
   - Console requires RoE document before engagement activation
   - Digital signatures link actions to authorization

---

## 📜 Rules of Engagement (RoE) Requirements

Before deploying KYNEĒ, ensure your RoE includes:

- **Client Information**: Name, contact, authorization signatory
- **Scope**: IP ranges, domains, physical locations
- **Timeline**: Start/end dates, testing windows
- **Methods**: Allowed techniques, tools, and escalation paths
- **Exclusions**: Out-of-scope assets, prohibited actions
- **Data Handling**: Retention, encryption, destruction timelines
- **Incident Response**: Emergency contacts, stop-work triggers
- **Reporting**: Format, delivery method, timeline

See [`docs/legal/rules-of-engagement-template.md`](docs/legal/rules-of-engagement-template.md) for a starter template.

---

## 👥 Contributor Responsibilities

All contributors to KYNEĒ must:

- **Not contribute features that facilitate illegal use**
- **Report security vulnerabilities responsibly** (see [SECURITY.md](SECURITY.md))
- **Advocate for ethical security practices** in discussions and documentation
- **Refuse to assist in unauthorized deployments**

---

## 🚨 Reporting Misuse

If you become aware of KYNEĒ being used unethically or illegally:

1. **Do not engage directly** with the suspected violator
2. **Collect evidence** (screenshots, logs, public posts)
3. **Report to**: security@[project-domain] (or GitHub Security Advisory)
4. **Escalate to authorities** if criminal activity is suspected

---

## ⚖️ Legal Disclaimer

**USERS ARE SOLELY RESPONSIBLE FOR ENSURING LEGAL AUTHORIZATION.**

The KYNEĒ project and its contributors:

- Provide this software "as-is" without warranty
- Assume no liability for misuse or illegal deployments
- Are not responsible for damages resulting from unauthorized use
- Reserve the right to refuse support to users violating this policy

**Unauthorized computer access is illegal in most jurisdictions and may result in:**

- Criminal prosecution
- Civil liability
- Professional license revocation
- Financial penalties
- Imprisonment

---

## 🔄 Policy Updates

This policy may be updated to reflect:

- Changes in applicable laws
- Community feedback
- Emerging ethical standards in cybersecurity

Users are responsible for reviewing the policy periodically. Continued use after updates constitutes acceptance.

---

## 📞 Contact

Questions about ethical use? Contact:

- **Security/Ethics Issues**: security@[project-domain]
- **Legal Questions**: Consult your own legal counsel
- **General Discussion**: [GitHub Discussions](https://github.com/zebadee2kk/kynee/discussions)

---

**Last Updated**: February 24, 2026
