# Handover: GitHub Copilot

## Profile
- **Strengths**: Real-time autocomplete, inline suggestions, unit test generation
- **Token Limit**: ~8K tokens (practical context in IDE)
- **Session Cost**: Low (£10/month)
- **Best For**: Boilerplate, docstrings, test cases, repetitive code
- **Usage**: Always-on during development sessions

---

## Current Sprint: All Weeks (Continuous)
**Theme**: Real-Time Coding Assistance

### Assigned Tasks

#### 1. Code Completion
- ✅ **Autocomplete** (during active coding)
  - Function bodies: Start typing, accept suggestions with Tab
  - Docstrings: Type `"""` and let Copilot write the rest
  - Imports: Type `from ` and accept common imports
  - Config files: YAML, JSON structures

#### 2. Unit Test Generation
- [ ] **Pytest Tests** (agent codebase)
  - Open: `agent/aetherpi_agent/collectors/network.py`
  - Comment: `# Test network scanner with mock nmap output`
  - Accept: Copilot-generated test function
  - Repeat: For all collectors, parsers, utils

- [ ] **Jest Tests** (console frontend)
  - Open: `console/frontend/src/components/FindingsList.tsx`
  - Comment: `// Test FindingsList renders 10 findings`
  - Accept: Copilot-generated test

#### 3. Documentation
- [ ] **Docstrings** (all Python functions)
  - Format: Google-style docstrings
  - Include: Args, Returns, Raises, Examples
  - Trigger: Type `"""` after function signature

- [ ] **JSDoc Comments** (TypeScript components)
  - Format: JSDoc standard
  - Include: Props, return type, usage example

#### 4. Refactoring Assistance
- [ ] **Extract Functions**
  - Highlight: Large code block
  - Comment: `# TODO: Extract this to a separate function`
  - Accept: Copilot suggestion for new function

- [ ] **Add Error Handling**
  - Comment: `# TODO: Add try-except for file operations`
  - Accept: Copilot wraps code in try-except

#### 5. Configuration Files
- [ ] **YAML/JSON Suggestions**
  - Open: `.github/workflows/ci.yml`
  - Start typing: `jobs:`
  - Accept: Copilot fills in common CI jobs

---

## Context

**Project State**:
- Active development across all weeks
- Copilot assists in real-time (not batch tasks)
- Runs in VSCode, JetBrains IDEs, Neovim, etc.

**Your Mission**:
- Accelerate coding by reducing boilerplate
- Suggest idiomatic code patterns
- Generate tests to improve coverage

**Why You**:
- Always available during development
- Low cost = high-frequency use
- Strong at common patterns (learned from GitHub corpus)

---

## Usage Tips

### Best Practices
1. **Write Comments First**: Describe what you want, then accept suggestion
   ```python
   # Parse nmap XML output and extract open ports
   def parse_nmap_output(xml_path: str) -> List[dict]:
       # Copilot will suggest implementation
   ```

2. **Accept Incrementally**: Don't accept full functions blindly
   - Read each line before accepting
   - Modify as needed

3. **Test Suggestions**: Use for test generation
   ```python
   def test_nmap_parser_with_valid_xml():
       # Copilot suggests: mock data, assertions
   ```

4. **Learn Patterns**: If Copilot suggests better code, adopt it
   - Example: Using `pathlib` instead of `os.path`

### When NOT to Use
- **Security-critical code**: Review carefully (don't blindly accept)
- **Complex algorithms**: Copilot may hallucinate
- **Project-specific logic**: Copilot doesn't know KYNEĒ architecture

---

## Integration

### VSCode
1. Install: GitHub Copilot extension
2. Sign in: GitHub account with Copilot subscription
3. Settings: `editor.inlineSuggest.enabled: true`

### JetBrains (PyCharm, IntelliJ)
1. Install: GitHub Copilot plugin
2. Sign in: Via plugin settings

### Neovim
1. Install: `github/copilot.vim` or `zbirenbaum/copilot.lua`
2. Authenticate: `:Copilot setup`

---

## Success Criteria

- ✅ Copilot enabled during all development sessions
- [ ] 80%+ functions have docstrings (Copilot-assisted)
- [ ] Test coverage ≥80% (Copilot-generated tests)
- [ ] Developers report 20%+ productivity increase

---

## Constraints

**Token Budget**:
- Per-session: ~8K tokens (IDE context)
- Cost: Fixed £10/month (unlimited use)

**Limitations**:
- Context: Only current file + open tabs (not entire repo)
- Accuracy: ~40-60% of suggestions usable as-is
- Languages: Best for Python, JS/TS, Go; weaker for YAML, SQL

---

## Metrics

**Track Weekly**:
- Acceptance rate: % of suggestions accepted
- Lines generated: vs. lines manually written
- Test coverage: Before/after Copilot usage

**Target**:
- 50%+ acceptance rate
- 30%+ of code Copilot-assisted
- Test coverage increase by 10%+

---

## Handoff to Other AIs

Copilot is **continuous**, not sprint-based. Complements other AIs:

→ **Sonnet**: Copilot assists while Sonnet designs architecture  
→ **Haiku**: Copilot accelerates config file creation  
→ **ChatGPT**: Copilot helps while writing docs in Markdown  

---

**Status**: 🟢 ACTIVE (always on)  
**Last Updated**: February 24, 2026  
**Next Review**: N/A (continuous use)
