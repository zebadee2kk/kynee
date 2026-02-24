# Getting Started

This guide helps new contributors set up a local development environment and make a first contribution.

**Important:** KYNEE is for authorized security assessments only. Read the ethical policy before you begin: [ETHICAL_USE_POLICY.md](../ETHICAL_USE_POLICY.md).

---

## Prerequisites

- **Python**: 3.11+
- **Node.js**: 20+
- **Git**: 2.40+
- **VS Code** (recommended)
- **Hardware** (optional): Raspberry Pi 3 B+ or better for agent testing

---

## Clone the Repository

```bash
git clone https://github.com/zebadee2kk/kynee.git
cd kynee
```

---

## Python Setup (Agent + Console Backend)

Create a virtual environment and install dependencies when available.

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -U pip
```

**Note:** Python package manifests may be added later in Week 3-5.

---

## Node.js Setup (Console Frontend)

```bash
cd console/frontend
npm install
```

---

## Open the VS Code Workspace

```bash
code .vscode/kynee.code-workspace
```

This loads separate folders for agent, console backend, console frontend, docs, and hardware.

---

## Run Tests (When Available)

```bash
# Agent tests
cd agent
pytest tests/ -v

# Console backend tests
cd console/backend
pytest tests/ -v

# Console frontend tests
cd console/frontend
npm test
```

---

## Make Your First Contribution

1. Read the contribution rules: [CONTRIBUTING.md](../CONTRIBUTING.md).
2. Create a short-lived branch:
   ```bash
   git checkout -b docs/getting-started-update
   ```
3. Make your changes.
4. Run formatting and tests (if applicable).
5. Commit using Conventional Commits:
   ```bash
   git commit -m "docs(getting-started): add setup steps"
   ```
6. Open a PR and follow the template.

---

## Troubleshooting

**Python not found**
- Ensure Python 3.11+ is installed and on PATH.

**Node version mismatch**
- Use `nvm` or `fnm` to install Node 20+.

**Permission errors on Windows**
- Run the terminal as Administrator when installing dependencies.

**Markdown links broken**
- Use relative links from the current file location.

---

## Get Help

- Read the roadmap for context: [ROADMAP.md](../ROADMAP.md)
- Check open issues: https://github.com/zebadee2kk/kynee/issues
- Ask questions in discussions: https://github.com/zebadee2kk/kynee/discussions
