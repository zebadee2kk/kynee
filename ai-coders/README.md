# AI Coder Coordination System

## Purpose

This directory contains handover files and task assignments for multiple AI coding assistants working collaboratively on KYNEĒ. Each AI has unique strengths, token limits, and cost profiles—this system optimizes their use.

---

## AI Coder Roster

| AI Assistant | Strengths | Best For | Token Limit | Cost Profile |
|--------------|-----------|----------|-------------|-------------|
| **Claude Opus 4.6** | Architecture, security, complex logic | System design, threat modeling | 1M tokens | High (£100-200/mo) |
| **Claude Sonnet 4.5** | Coding, debugging, refactoring | Core agent/console development | 200K-1M tokens | Medium (£20/mo) |
| **Claude Haiku** | Fast, simple tasks, boilerplate | Config files, basic scripts | 200K tokens | Low (API £/1M tokens) |
| **ChatGPT (GPT-5.2)** | Natural language, docs, tutorials | Documentation, user guides | 128K tokens | Medium (£20/mo) |
| **ChatGPT Codex (5.3)** | Agentic coding, multi-file edits | Complex refactors, CI/CD | 128K tokens | Included in Plus |
| **Grok 4.1 Heavy** | Massive context, research | Multi-repo analysis, codebases | 2M tokens | High (£300/mo) |
| **Gemini 1.5 Pro** | Google ecosystem, data analysis | BigQuery, analytics, Python ML | 1M tokens | Variable (API) |
| **GitHub Copilot** | In-IDE autocomplete, snippets | Real-time coding, boilerplate | 8K tokens (practical) | Low (£10/mo) |
| **VSCode + Copilot** | Integrated IDE workflow | Inline suggestions, unit tests | 8K tokens | Low (£10/mo) |

---

## Handover Files

Each AI has a dedicated handover file with:
- **Current sprint tasks** (week-aligned with ROADMAP.md)
- **Context summary** (what's been done, what's next)
- **File inventory** (relevant codebase locations)
- **Constraints** (token budget, cost limits, session length)
- **Success criteria** (how to verify completion)

### Files

1. [`handover-claude-opus.md`](handover-claude-opus.md) — Architecture & security
2. [`handover-claude-sonnet.md`](handover-claude-sonnet.md) — Core development
3. [`handover-claude-haiku.md`](handover-claude-haiku.md) — Quick tasks & configs
4. [`handover-chatgpt.md`](handover-chatgpt.md) — Documentation & guides
5. [`handover-chatgpt-codex.md`](handover-chatgpt-codex.md) — Agentic coding
6. [`handover-grok.md`](handover-grok.md) — Large context analysis
7. [`handover-gemini.md`](handover-gemini.md) — Data & analytics
8. [`handover-copilot.md`](handover-copilot.md) — IDE autocomplete
9. [`handover-vscode.md`](handover-vscode.md) — Integrated development

---

## Task Allocation Strategy

### Phase 1: Architecture & Planning (Week 1)
- **Claude Opus**: ADRs, threat model, system design
- **ChatGPT**: Expand documentation, write tutorials
- **Haiku**: Generate config templates, boilerplate

### Phase 2: Core Development (Weeks 2-5)
- **Claude Sonnet**: Agent collectors, console backend
- **Codex**: Multi-file refactors, CI/CD pipelines
- **Copilot**: Real-time code completion during development
- **Gemini**: Data schema design, analytics queries

### Phase 3: Integration & Testing (Weeks 6-7)
- **Grok**: Full codebase review (2M token context)
- **Sonnet**: AI assistant module, integration tests
- **Copilot**: Unit test generation

### Phase 4: Hardening & Release (Week 8)
- **Opus**: Security review, threat mitigation
- **ChatGPT**: Final documentation polish
- **Haiku**: Deployment scripts, Docker configs

---

## Workflow

### Daily
1. Check current week in `ROADMAP.md`
2. Review relevant handover file(s)
3. Complete assigned tasks
4. Update handover file with progress
5. Commit changes to feature branch

### Weekly
1. Sprint review (all AI outputs)
2. Update handover files for next week
3. Merge completed features to `main`
4. Tag milestone (e.g., `v0.1-week3`)

### Handoff Protocol
1. AI completes task
2. Updates handover file:
   - Mark task as DONE
   - Add "Next AI" note if continuation needed
   - List any blockers or dependencies
3. Commit with message: `chore(ai-handover): <AI-name> completed <task>`

---

## Token Budget Management

### High-Cost AIs (Opus, Grok)
- Reserve for **complex, high-value tasks** only
- Batch work to minimize session churn
- Use cheaper AIs for iteration/refinement

### Medium-Cost AIs (Sonnet, ChatGPT, Gemini)
- Primary workhorses for development
- Suitable for most coding tasks
- Balance quality vs. cost

### Low-Cost AIs (Haiku, Copilot)
- High-frequency, low-complexity tasks
- Boilerplate, configs, simple scripts
- Real-time in-IDE assistance

---

## Quality Gates

**Before Committing**:
- [ ] Code passes linting (`ruff`, `eslint`)
- [ ] Tests pass (`pytest`, `npm test`)
- [ ] Follows project style guide
- [ ] No secrets committed (check `.gitignore`)
- [ ] Handover file updated

**Before Merging**:
- [ ] PR reviewed by human maintainer
- [ ] CI/CD pipeline passes
- [ ] Documentation updated (if user-facing)
- [ ] Changelog entry added (if significant)

---

## Emergency Escalation

**If an AI encounters:**
- **Blocker**: Complex architectural decision
- **Security concern**: Potential vulnerability
- **Legal question**: Compliance or ethical issue

**Action**: Stop work, document issue in handover file, alert human maintainer (@zebadee2kk)

---

## Adding New AIs

To add a new AI assistant:

1. Create `handover-<ai-name>.md` using template below
2. Update this README with AI's profile
3. Assign initial tasks based on strengths
4. Add to weekly sprint planning

### Handover Template

```markdown
# Handover: <AI Name>

## Profile
- **Strengths**: <list>
- **Token Limit**: <number>
- **Session Cost**: <estimate>
- **Best For**: <use cases>

## Current Sprint: Week X
**Dates**: <start> - <end>

### Assigned Tasks
- [ ] Task 1
- [ ] Task 2

### Context
<Summary of what's been done, what this AI needs to know>

### Files to Work On
- `path/to/file1.py`
- `path/to/file2.ts`

### Success Criteria
- Metric 1
- Metric 2

### Blockers
- None / <list>

### Notes for Next Session
<Anything the AI should remember next time>
```

---

**Last Updated**: February 24, 2026  
**Coordinator**: @zebadee2kk
