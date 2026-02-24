# KYNEĒ Project Governance

## Purpose

This document defines how the KYNEĒ project is governed, including decision-making processes, roles, and contribution guidelines.

---

## Governance Model

KYNEĒ uses a **meritocratic** governance model:

- **Contributors**: Anyone who submits accepted PRs
- **Committers**: Contributors with sustained contributions (3+ merged PRs)
- **Maintainers**: Committers with commit access and voting rights
- **Lead Maintainer**: Final decision-maker (currently @zebadee2kk)

---

## Roles & Responsibilities

### Contributors

**Who**: Anyone who contributes code, docs, or bug reports.

**Responsibilities**:
- Follow [Ethical Use Policy](ETHICAL_USE_POLICY.md) and [Code of Conduct](CODE_OF_CONDUCT.md)
- Submit PRs adhering to [Contributing Guidelines](CONTRIBUTING.md)
- Respond to review feedback within 7 days

**Privileges**:
- Open issues and PRs
- Participate in Discussions

### Committers

**Who**: Contributors with 3+ merged PRs demonstrating consistent quality.

**Responsibilities**:
- Review PRs in their area of expertise
- Triage issues (add labels, request info)
- Mentor new contributors

**Privileges**:
- "Committer" badge in GitHub
- Invited to private maintainer discussions (optional)

**Nomination**: Any maintainer can nominate a contributor. Requires majority maintainer vote.

### Maintainers

**Who**: Committers with sustained contributions (6+ months, 10+ merged PRs) and demonstrated technical leadership.

**Responsibilities**:
- Review and merge PRs
- Enforce quality standards (tests, docs, security)
- Participate in roadmap planning
- Respond to security issues within 48 hours
- Represent project in public forums

**Privileges**:
- Commit access to `main` (via PR approval)
- Voting rights on major decisions
- Access to private security vulnerability reports

**Nomination**: Existing maintainers nominate via private discussion. Requires 2/3 majority vote.

### Lead Maintainer

**Who**: Project founder or elected lead (currently @zebadee2kk).

**Responsibilities**:
- Break ties in maintainer votes
- Make final decisions on contentious issues
- Release management (version bumps, tags)
- Security incident coordination
- Legal/compliance decisions

**Term**: Lead maintainer serves indefinitely unless:
- They resign
- Maintainers vote to remove (requires 75% supermajority)

---

## Decision-Making

### Consensus-Seeking

For routine decisions (features, bug fixes, docs):
1. Propose via issue or PR
2. Discuss in comments (aim for 3+ days for major changes)
3. Merge if no blocking objections from maintainers

### Voting

For major decisions (architecture changes, security policies, governance changes):
1. Propose via GitHub Discussion
2. Allow 7 days for feedback
3. Maintainers vote (comment "+1", "0", "-1")
4. Requires **majority** (50% + 1) to pass
5. Lead maintainer breaks ties

**Major Decisions Requiring Vote**:
- Adding/removing core dependencies
- Changing security policies
- Modifying Ethical Use Policy
- Governance changes
- Trademark/licensing changes

### Emergency Decisions

For security vulnerabilities or critical bugs:
- Lead maintainer or any 2 maintainers can make immediate decisions
- Post-hoc review within 7 days

---

## Code of Conduct Enforcement

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for full policy.

**Process**:
1. Report violations to: [INSERT CONTACT EMAIL]
2. Maintainers review within 48 hours
3. Decisions follow escalation ladder:
   - Warning (private message)
   - Temporary ban (7-30 days)
   - Permanent ban
4. Appeals handled by lead maintainer (final)

---

## Intellectual Property

### Copyright

All contributions are licensed under Apache 2.0 (see [LICENSE](LICENSE)).

By submitting a PR, contributors agree:
- They own the copyright or have permission to contribute
- The contribution is licensed under Apache 2.0
- They waive moral rights (where applicable)

### Contributor License Agreement (CLA)

Currently **not required**. If the project grows, we may adopt [Apache ICLA](https://www.apache.org/licenses/icla.pdf).

### Trademarks

"KYNEĒ" and the project logo (if created) are trademarks of the KYNEĒ Project.

**Acceptable Use**:
- Referring to the project ("I use KYNEĒ for pentesting")
- Unmodified distributions
- Community events ("KYNEĒ User Meetup")

**Prohibited Use**:
- Implying official endorsement without permission
- Commercial products using "KYNEĒ" in name without permission

---

## Roadmap & Planning

### Quarterly Planning

Maintainers meet every 3 months (virtual) to:
- Review roadmap progress
- Prioritize backlog
- Assign major features
- Plan releases

**Public**: Meeting notes published in [GitHub Discussions](https://github.com/zebadee2kk/kynee/discussions).

### Release Cycle

- **Minor releases** (0.x): Every 2-4 weeks during active development
- **Major releases** (1.0, 2.0): Based on feature completeness
- **Patch releases** (x.y.z): As needed for critical bugs/security

---

## Conflict Resolution

1. **Technical Disagreements**: Resolve via discussion, fallback to maintainer vote.
2. **Personal Conflicts**: Mediated by neutral maintainer, escalate to lead if unresolved.
3. **Code of Conduct Violations**: See enforcement process above.

---

## Amendments

This governance document may be amended via:
1. PR to `GOVERNANCE.md`
2. Discussion period (14 days)
3. Maintainer vote (requires 2/3 supermajority)

---

## Contact

- **General Inquiries**: [GitHub Discussions](https://github.com/zebadee2kk/kynee/discussions)
- **Security Issues**: See [SECURITY.md](SECURITY.md)
- **Code of Conduct**: [INSERT CONTACT EMAIL]
- **Legal/Licensing**: [INSERT CONTACT EMAIL]

---

**Version**: 1.0  
**Effective Date**: February 24, 2026  
**Last Reviewed**: February 24, 2026
