# Contributing to KYNEĒ

Thank you for your interest in contributing to KYNEĒ! We welcome contributions from security professionals, developers, and researchers who share our commitment to ethical security practices.

---

## 📜 Prerequisites

Before contributing, please:

1. Read and agree to our [**Ethical Use Policy**](ETHICAL_USE_POLICY.md)
2. Review the [**Code of Conduct**](CODE_OF_CONDUCT.md)
3. Understand the [**Security Policy**](SECURITY.md)
4. Familiarize yourself with the [**Roadmap**](ROADMAP.md)

---

## 🛠️ Types of Contributions

We accept:

- **Bug fixes**: Correctness, security, or stability issues
- **New features**: Enhancements aligned with the roadmap
- **Documentation**: Guides, tutorials, API docs, or clarifications
- **Testing**: Unit tests, integration tests, or security test cases
- **Hardware compatibility**: Verified adapter/device configurations
- **Security improvements**: Hardening, threat modeling, or vulnerability reports

**We do NOT accept**:

- Features that facilitate unauthorized access
- Autonomous exploitation capabilities (all actions require human approval)
- Obfuscation or anti-forensics features
- Contributions that violate our Ethical Use Policy

---

## 👣 Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/kynee.git
cd kynee
git remote add upstream https://github.com/zebadee2kk/kynee.git
```

### 2. Set Up Development Environment

```bash
# Agent (Python)
cd agent
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# Console Backend (Python)
cd console/backend
pip install -e ".[dev]"

# Console Frontend (Node.js)
cd console/frontend
npm install
```

### 3. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

---

## ✍️ Making Changes

### Code Style

- **Python**: Follow PEP 8, use `black` for formatting, `ruff` for linting
- **JavaScript/TypeScript**: Follow Airbnb style guide, use ESLint + Prettier
- **Go**: Follow `gofmt` and `golangci-lint` conventions

```bash
# Python
black .
ruff check .

# JavaScript
npm run lint
npm run format
```

### Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(agent): add Bluetooth discovery module
fix(console): resolve CSRF token validation bug
docs(legal): clarify RoE template language
test(transport): add WireGuard handshake tests
```

### Testing

- Write tests for all new features
- Ensure existing tests pass: `pytest` (Python), `npm test` (JS)
- Aim for >80% code coverage on security-critical modules

```bash
# Python
pytest tests/ --cov=aetherpi_agent

# JavaScript
npm test -- --coverage
```

---

## 📦 Submitting a Pull Request

### 1. Push Your Branch

```bash
git push origin feature/your-feature-name
```

### 2. Open a Pull Request

- Go to [https://github.com/zebadee2kk/kynee/pulls](https://github.com/zebadee2kk/kynee/pulls)
- Click "New Pull Request"
- Select your branch
- Fill out the PR template (description, testing, checklist)

### 3. PR Requirements

Your PR must:

- [ ] Pass all CI checks (linting, tests, security scans)
- [ ] Include tests for new functionality
- [ ] Update documentation (if user-facing)
- [ ] Reference related issues (`Fixes #123`, `Closes #456`)
- [ ] Include a changelog entry (if significant)
- [ ] Affirm compliance with Ethical Use Policy

### 4. Review Process

- Maintainers will review within 7 days
- Address feedback in new commits (do not force-push)
- Once approved, maintainers will merge using squash or rebase

---

## 🐛 Reporting Bugs

**Security vulnerabilities**: See [SECURITY.md](SECURITY.md) (private disclosure).

**Non-security bugs**: Open a [GitHub Issue](https://github.com/zebadee2kk/kynee/issues/new/choose) with:

- KYNEĒ version
- Hardware (if agent-related)
- Steps to reproduce
- Expected vs. actual behavior
- Logs (redact sensitive info)

---

## 💡 Requesting Features

Open a [Feature Request](https://github.com/zebadee2kk/kynee/issues/new/choose) with:

- **Use case**: Why is this needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**: Other approaches
- **Ethical considerations**: Does it comply with our policy?

---

## 📝 Documentation Contributions

Documentation is as valuable as code! To contribute:

- Improve existing docs in `docs/`
- Add tutorials or examples
- Clarify confusing language
- Fix typos or broken links

Same PR process applies.

---

## 🤝 Community Guidelines

- **Be respectful**: Constructive criticism only
- **Be patient**: Maintainers are volunteers
- **Be ethical**: No discussions of illegal techniques
- **Be collaborative**: Help others in Discussions

---

## 🎓 Learning Resources

New to contributing? Check out:

- [How to Contribute to Open Source](https://opensource.guide/how-to-contribute/)
- [First Timers Only](https://www.firsttimersonly.com/)
- [GitHub's Pull Request Guide](https://docs.github.com/en/pull-requests)

---

## 🏆 Recognition

Contributors are recognized in:

- [`CONTRIBUTORS.md`](CONTRIBUTORS.md) (alphabetical listing)
- Release notes for significant contributions
- Security Hall of Fame (for vulnerability reports)

---

## ❓ Questions?

- **General Questions**: [GitHub Discussions](https://github.com/zebadee2kk/kynee/discussions)
- **Technical Help**: Tag `@maintainers` in an issue
- **Private Inquiries**: [INSERT CONTACT EMAIL]

---

**Thank you for helping make KYNEĒ a professional, ethical, and powerful tool for the security community!**
