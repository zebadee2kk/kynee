# Support

## Getting Help

### Before Asking for Help

Please check:

1. **Documentation**: [`docs/`](docs/) and [`README.md`](README.md)
2. **Existing Issues**: [Search open/closed issues](https://github.com/zebadee2kk/kynee/issues)
3. **Discussions**: [Search community discussions](https://github.com/zebadee2kk/kynee/discussions)

---

## Support Channels

### GitHub Discussions (Recommended)

Best for:

- General questions
- How-to inquiries
- Feature ideas
- Community chat

[Start a discussion →](https://github.com/zebadee2kk/kynee/discussions)

### GitHub Issues

Best for:

- Bug reports (use [bug_report.yml](.github/ISSUE_TEMPLATE/bug_report.yml))
- Feature requests (use [feature_request.yml](.github/ISSUE_TEMPLATE/feature_request.yml))
- Security questions (use [security_question.yml](.github/ISSUE_TEMPLATE/security_question.yml))

**DO NOT** report security vulnerabilities as public issues. See [SECURITY.md](SECURITY.md).

[Open an issue →](https://github.com/zebadee2kk/kynee/issues/new/choose)

---

## Common Questions

### Installation & Setup

**Q: Which Raspberry Pi models are supported?**  
A: Pi 3 Model B/B+ (reference platform), Pi 4, and Pi Zero 2 W. See [hardware/compatibility-matrix.md](hardware/compatibility-matrix.md).

**Q: Where can I buy compatible Wi-Fi adapters?**  
A: See [hardware/bill-of-materials.md](hardware/bill-of-materials.md) for tested models and suppliers.

**Q: How do I build the Kali Linux image?**  
A: See [docs/build/kali-rpi3-minimal.md](docs/build/kali-rpi3-minimal.md) (to be completed in Week 2).

### Legal & Ethical Use

**Q: Can I use KYNEĒ for bug bounties?**  
A: Yes, if the bug bounty program explicitly authorizes this type of testing. Always read the program's rules.

**Q: Can I use KYNEĒ on my home network?**  
A: Yes, you own your home network. However, be aware of ISP terms of service.

**Q: What if I accidentally scan out-of-scope targets?**  
A: KYNEĒ has policy enforcement to prevent this, but if it happens:
1. Stop testing immediately
2. Notify the client
3. Document the incident in your audit log
4. Follow your RoE incident response procedures

See [ETHICAL_USE_POLICY.md](ETHICAL_USE_POLICY.md) and [docs/legal/scope-and-authorization.md](docs/legal/scope-and-authorization.md).

### Technical Issues

**Q: Agent won't connect to console**  
A: Check:
1. WireGuard configuration (`wg show`)
2. Firewall rules (UDP 51820)
3. Console endpoint reachable (`ping console.example.com`)
4. Try HTTPS fallback mode

See [docs/architecture/adr-0002-transport-design.md](docs/architecture/adr-0002-transport-design.md).

**Q: Flipper Zero not detected**  
A: See [hardware/flipper/integration-notes.md](hardware/flipper/integration-notes.md) troubleshooting section.

---

## Response Times

**Community Support** (GitHub Discussions):

- Best-effort, typically within 24-48 hours
- Faster for simple questions

**Bug Reports** (GitHub Issues):

- Acknowledged within 7 days
- Critical bugs: Patched within 7-14 days
- Non-critical: Triaged for upcoming releases

**Security Vulnerabilities** (Private disclosure):

- Acknowledged within 48 hours
- See [SECURITY.md](SECURITY.md) for SLAs

---

## Commercial Support

**Professional services** are not yet available but are planned for post-1.0.

Interested organizations can express interest in [GitHub Discussions](https://github.com/zebadee2kk/kynee/discussions) with the `business` tag.

---

## Contributing Back

The best way to get support is to contribute:

- Answer questions in Discussions
- Improve documentation
- Submit bug fixes
- Share hardware compatibility findings

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Resources

- **Documentation**: [`docs/`](docs/)
- **Roadmap**: [ROADMAP.md](ROADMAP.md)
- **Legal/Compliance**: [docs/legal/](docs/legal/)
- **Hardware**: [hardware/](hardware/)
- **Architecture**: [docs/architecture/](docs/architecture/)

---

**Last Updated**: February 24, 2026  
**Maintainer**: @zebadee2kk
