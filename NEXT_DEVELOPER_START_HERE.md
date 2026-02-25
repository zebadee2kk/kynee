# 🚀 Next Developer: Start Here

**Date**: February 25, 2026  
**Status**: Week 2 Complete (90%) — Ready for Week 3  
**Your Mission**: Choose one of three paths below

---

## 📊 TL;DR Project Status

- ✅ **Week 1 Foundation**: 100% complete (governance, schemas, CI/CD)
- ✅ **Week 2 Core Modules**: 90% complete (policy, audit, coordinator)
- ✅ **Test Coverage**: 81.98% with 74 passing tests
- ⏸️ **CLI**: Scaffolded but not implemented
- ⭕ **Collectors**: Not started (Week 3 priority)

**Bottom Line**: Rock-solid foundation. Ready to build features.

---

## 📚 What to Read First

### Must Read (In Order)

1. **[WEEK2_COMPLETION_REVIEW.md](WEEK2_COMPLETION_REVIEW.md)** — Complete project assessment (this file)
2. **[WEEK2_HANDOVER.md](WEEK2_HANDOVER.md)** — Technical guide to core modules
3. **[ROADMAP.md](ROADMAP.md)** — 8-week development timeline

### Reference as Needed

- [HANDOVER.md](HANDOVER.md) — Week 1-2 summary
- [docs/architecture/](docs/architecture/) — 4 Architecture Decision Records
- [agent/tests/unit/](agent/tests/unit/) — Test patterns and examples

---

## 🛫 Quick Setup

```bash
# Clone and setup
git clone https://github.com/zebadee2kk/kynee.git
cd kynee/agent

# Create virtual environment
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Verify setup (should see 74 tests pass)
pytest tests/unit/ -v --cov=kynee_agent

# Expected: 74 passed, 81.98% coverage
```

**Stuck?** Open a GitHub issue with label `question`.

---

## ⚡ Three Development Options

### Option 1: Complete Week 2 (CLI) ⭐ CLEAN MILESTONE

**What**: Implement 4 CLI commands (`create`, `plan`, `list`, `status`)  
**Timeline**: 2-3 days  
**Best For**: Clean Week 2 completion before Week 3  
**Handover Prompt**: See [WEEK2_COMPLETION_REVIEW.md → Option 1](WEEK2_COMPLETION_REVIEW.md#option-1-complete-week-2-cli-focus--recommended)

```bash
# Create feature branch
git checkout -b feature/cli-implementation

# Implement in agent/kynee_agent/cli/main.py
# Reference: tests/unit/test_coordinator.py for patterns

# Test
pytest tests/unit/test_cli.py -v --cov=kynee_agent.cli
```

---

### Option 2: Begin Week 3 (Collectors) 🔥 FASTEST VALUE

**What**: Implement 3 scan collectors (network, wireless, Bluetooth)  
**Timeline**: 5-7 days  
**Best For**: Maximum velocity, defer CLI  
**Handover Prompt**: See [WEEK2_COMPLETION_REVIEW.md → Option 2](WEEK2_COMPLETION_REVIEW.md#option-2-begin-week-3-collectors--fastest-path)

```bash
# Create feature branch
git checkout -b feature/collectors-implementation

# Implement in agent/kynee_agent/collectors/
# - network.py (nmap wrapper)
# - wireless.py (airodump-ng wrapper)
# - bluetooth.py (hcitool wrapper)

# CRITICAL: All collectors MUST:
# 1. Validate with PolicyEngine before scanning
# 2. Log to AuditLogWriter
# 3. Return JSON matching schemas/findings.schema.json

# Test
pytest tests/unit/test_network_collector.py -v
```

---

### Option 3: Parallel (CLI + Collectors) ⚡ MAX SPEED

**What**: Both tracks simultaneously  
**Timeline**: 1 week (parallel)  
**Best For**: Multiple developers/agents available  
**Details**: See [WEEK2_COMPLETION_REVIEW.md → Option 3](WEEK2_COMPLETION_REVIEW.md#option-3-parallel-development--maximum-velocity)

**Split Work**:
- **Track 1**: Human developer implements CLI (2-3 days)
- **Track 2**: AI agent implements collectors (5-7 days)
- **Merge**: CLI first, then collectors

---

## ⚠️ Critical Rules

These patterns are **MANDATORY** for all new code:

### 1. Policy Validation (Always)
```python
# ✅ CORRECT
self.policy_engine.validate_scan_request(method, target)
# Then proceed with operation

# ❌ WRONG
result = self._scan(target)  # Missing validation!
```

### 2. Audit Logging (Always)
```python
# ✅ CORRECT
self.audit_log.log_scan_started(agent_id, scan_id, method, target)

# ❌ WRONG
result = self._scan(target)  # Missing audit trail!
```

### 3. Type Hints (Always)
```python
# ✅ CORRECT
async def scan(self, target: dict[str, Any]) -> dict[str, Any]:
    ...

# ❌ WRONG
async def scan(self, target):  # No types!
    ...
```

### 4. Async for I/O (Always)
```python
# ✅ CORRECT
proc = await asyncio.create_subprocess_exec("nmap", target)
stdout, _ = await proc.communicate()

# ❌ WRONG
result = subprocess.run(["nmap", target])  # Blocking!
```

---

## ✅ Success Criteria

Before submitting your PR, verify:

### For CLI Implementation
- [ ] All 4 commands functional (`create`, `plan`, `list`, `status`)
- [ ] Wired to AgentCoordinator
- [ ] Unit tests >80% coverage
- [ ] Help text clear and accurate
- [ ] Works on Linux/macOS/Windows

### For Collectors Implementation
- [ ] All 3 collectors implemented (network, wireless, Bluetooth)
- [ ] Each validates with PolicyEngine before execution
- [ ] Each logs to AuditLogWriter
- [ ] Output matches `schemas/findings.schema.json`
- [ ] >80% test coverage per collector
- [ ] All tests passing

### General Requirements
- [ ] Code passes `black .` (formatting)
- [ ] Code passes `ruff check .` (linting)
- [ ] Code passes `mypy .` (type checking)
- [ ] All unit tests pass: `pytest tests/unit/ -v`
- [ ] Coverage >80%: `pytest --cov=kynee_agent`
- [ ] Documentation updated (docstrings, README if needed)
- [ ] Commit messages follow convention: `feat(area): description`

---

## 📞 Need Help?

### Common Issues

**Q: Tests fail with "ImportError: No module named kynee_agent"**  
A: Install in dev mode: `pip install -e ".[dev]"`

**Q: Mypy errors on datetime operations**  
A: Known deprecation warnings (Python 3.12+). Suppress with `# type: ignore` for now.

**Q: How do I add a new module?**  
A: Follow existing patterns:
1. Create module in appropriate subpackage
2. Add full docstrings and type hints
3. Create test file with >80% coverage
4. Update `__init__.py` exports
5. Run `pytest tests/unit/ --cov` to verify

### Get Support

- **GitHub Issues**: Open issue with appropriate label
- **Documentation**: Check WEEK2_HANDOVER.md for technical details
- **Code Examples**: Review `tests/unit/` for patterns
- **Architecture**: Read ADRs in `docs/architecture/`

---

## 👋 Before You Start

1. ✅ **Read WEEK2_COMPLETION_REVIEW.md** (full project assessment)
2. ✅ **Choose your path** (CLI, Collectors, or Parallel)
3. ✅ **Set up environment** (see Quick Setup above)
4. ✅ **Verify tests pass** (should see 74 passing)
5. ✅ **Create feature branch** (per chosen path)
6. ✅ **Read relevant handover prompt** (in WEEK2_COMPLETION_REVIEW.md)
7. ✅ **Begin implementation** (follow mandatory patterns)

---

## 🏆 Final Notes

**Quality Bar**: The existing code sets a high standard (81.98% coverage, full type hints, comprehensive tests). Match this quality in your contributions.

**Timeline**: Be realistic. CLI is 2-3 days, Collectors are 5-7 days for a reason. Don't rush—quality matters.

**Communication**: Open issues early if you're stuck. Better to ask than to implement incorrectly.

**Testing**: Write tests as you code, not after. Aim for >80% coverage from the start.

---

**Welcome to KYNEĒ development!** The foundation is solid. Time to build features. 🚀

**Last Updated**: February 25, 2026  
**Maintainer**: @zebadee2kk  
**Questions**: Open a GitHub issue with label `question`
