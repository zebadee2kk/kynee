# 🚀 KYNEĒ Development Guide

**Quick reference for setting up and contributing to KYNEĒ.**

---

## ⚡ 5-Minute Setup

### All Components

```bash
# 1. Clone repository
git clone https://github.com/zebadee2kk/kynee.git
cd kynee

# 2. Open VS Code workspace
code .vscode/kynee.code-workspace

# 3. Install dependencies (choose one or more)

# Agent
cd agent && python3.11 -m venv venv && source venv/bin/activate && pip install -e ".[dev]" && cd ..

# Console Backend
cd console/backend && python3.11 -m venv venv && source venv/bin/activate && pip install -e ".[dev]" && cd ../..

# Console Frontend
cd console/frontend && npm install && cd ../..

# 4. Run local development servers

# Terminal 1: Agent tests
cd agent && pytest tests/ -v

# Terminal 2: Backend
cd console/backend && python -m kynee_console_backend.main

# Terminal 3: Frontend
cd console/frontend && npm run dev

# Open http://localhost:5173 in browser
```

---

## 📁 Directory Quick Reference

| Path | Purpose | Language | Status |
|------|---------|----------|--------|
| `agent/` | Raspberry Pi autonomous agent | Python | Week 1-2 scaffold ✅ |
| `console/backend/` | REST API server | Python | Week 1-2 scaffold ✅ |
| `console/frontend/` | Web UI | TypeScript/React | Week 1-2 scaffold ✅ |
| `docs/` | Documentation & guides | Markdown | Complete ✅ |
| `schemas/` | JSON Schema data contracts | JSON | Validated ✅ |
| `infra/` | Docker, Terraform, WireGuard | YAML/HCL | Empty (Week 5) |
| `hardware/` | Bill of materials, compatibility | Markdown | Planned (Week 2) |

---

## 🔄 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feat/agent-collectors-network
# or
git checkout -b feat/console-backend-engagements-api
# or
git checkout -b feat/console-frontend-findings-dashboard
```

**Naming**: `<type>/<area>-<description>`
- `type`: feat, fix, docs, chore, test
- `area`: agent, console-backend, console-frontend, docs, infra, hardware
- `description`: lowercase, hyphens

### 2. Make Changes

**Python (Agent & Backend)**
```bash
# Code formatting
black .

# Linting
ruff check . --fix

# Type checking
mypy .

# Tests
pytest tests/ -v --cov
```

**TypeScript (Frontend)**
```bash
# Linting
npm run lint

# Formatting
npx prettier --write src/

# Type checking
npm run type-check

# Tests
npm test
```

### 3. Commit with Conventional Commits

```bash
git commit -m "feat(agent): add network collector with nmap

- Implemented NetworkCollector class
- Added subnet scanning capability
- Integrated with findings schema
- Added 12 unit tests

Closes #42"
```

### 4. Push & Open PR

```bash
git push origin feat/agent-collectors-network
# Then go to GitHub and open a PR using the template
```

### 5. Review & Merge

- Ensure CI checks pass (linting, tests, security scan)
- Get at least 1 approval
- Squash or rebase & merge (no merge commits)

---

## 🧪 Testing Guidelines

### Agent (Python)

```bash
cd agent

# All tests
pytest tests/ -v

# Specific test file
pytest tests/unit/test_agent.py -v

# With coverage
pytest tests/ --cov=kynee_agent --cov-report=html

# Watch mode (requires pytest-watch)
ptw tests/ -v
```

**Expected**: >80% code coverage

### Console Backend (Python)

```bash
cd console/backend

# All tests
pytest tests/ -v

# API endpoint tests
pytest tests/test_routers/ -v

# With coverage
pytest --cov=kynee_console_backend --cov-report=term-missing
```

### Console Frontend (TypeScript)

```bash
cd console/frontend

# All tests
npm test

# Watch mode
npm test -- --watch

# Coverage
npm test -- --coverage
```

---

## 🔍 Code Review Checklist

Before requesting review, ensure:

- [ ] All tests pass locally
- [ ] Code is formatted and linted
- [ ] Types check with mypy/tsc
- [ ] No console.log or print statements left
- [ ] No hardcoded secrets or credentials
- [ ] Docstrings/comments added for non-obvious logic
- [ ] Commit messages follow conventional commits
- [ ] PR description explains *why* changes were made
- [ ] Related GitHub issues are mentioned

---

## 🐛 Common Issues & Fixes

### Python ImportError

```
ModuleNotFoundError: No module named 'kynee_agent'
```

**Fix**: Install in development mode from the component directory:
```bash
cd agent
pip install -e .
```

### Node/npm version mismatch

```
npm ERR! Node v18.0.0 is not compatible with this package
```

**Fix**: Use nvm to switch Node version:
```bash
nvm use 20  # or whatever version package.json specifies
```

### Port already in use

```
Address already in use :::8000
```

**Fix**: Kill the process or use a different port:
```bash
# Find process
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
FASTAPI_PORT=8001 python -m kynee_console_backend.main
```

### Vite dev server not loading

```
GET http://localhost:5173/api/v1/health → 404
```

**Fix**: Ensure backend is running and check vite.config.ts proxy:
```bash
# Terminal 1
cd console/backend && python -m kynee_console_backend.main

# Terminal 2
cd console/frontend && npm run dev

# Check http://localhost:8000/health first
```

---

## 📚 Key Files to Know

### Architecture
- `docs/architecture/adr-*.md` — Design decisions

### Core Logic
- `agent/kynee_agent/core/agent.py` — Agent lifecycle
- `console/backend/kynee_console_backend/app/__init__.py` — API setup
- `console/frontend/src/App.tsx` — Frontend routing

### Data Models
- `agent/kynee_agent/models/*.py` — Agent data structures
- `console/backend/kynee_console_backend/schemas/*.py` — API schemas
- `schemas/*.json` — JSON Schema contracts

### Configuration
- `agent/pyproject.toml` — Agent deps & tools
- `console/backend/pyproject.toml` — Backend deps & tools
- `console/frontend/package.json` — Frontend deps
- `.github/workflows/*.yml` — CI/CD pipelines

---

## 🤔 Before You Ask...

### "How do I X?"

1. Check the relevant README (`agent/README.md`, `console/README.md`)
2. Look at the ADRs (`docs/architecture/`)
3. Search existing tests for examples
4. Check the docstrings in the code
5. Ask in GitHub Issues/Discussions

### "Can I do Y?"

1. Read `docs/ops/branching-and-ai-collaboration.md`
2. Check CONTRIBUTING.md for our standards
3. If multiple AI agents are involved, use the handover system

### "What does this acronym mean?"

- **RoE**: Rules of Engagement (authorization contract)
- **ADR**: Architecture Decision Record
- **CI/CD**: Continuous Integration / Continuous Deployment
- **ORM**: Object-Relational Mapping (SQLAlchemy)
- **mTLS**: mutual TLS (two-way authentication)
- **WireGuard**: VPN protocol for secure agent-console communication

---

## 📞 Getting Help

- **Issues**: Use GitHub Issues for bugs and features
- **Discussions**: Use GitHub Discussions for questions
- **Security**: See SECURITY.md for vulnerability reporting
- **Ethics**: See ETHICAL_USE_POLICY.md before deploying

---

## 🎯 Development Roadmap

| Week | Focus | Deliverables |
|------|-------|--------------|
| 1-2 | Scaffolding | ✅ Complete |
| 3-4 | Agent Core | Collectors, policy, audit |
| 5 | Console v0 | Backend API, frontend UI |
| 6 | AI Assistant | Integration with console |
| 7-8 | Beta Release | Packaging, docs, deployment |

See [ROADMAP.md](../ROADMAP.md) for details.

---

## 🚀 Next Steps

1. **Choose your focus**: Agent, backend, or frontend
2. **Read the relevant README** for that component
3. **Set up your development environment** (see above)
4. **Check existing tests** for patterns
5. **Pick an issue** from GitHub or create one
6. **Follow the workflow** (branch → code → test → PR)
7. **Celebrate your contribution!** 🎉

---

**Happy coding!** If you have questions, open an issue on GitHub.

Last updated: February 24, 2026
