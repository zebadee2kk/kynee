# Handover: ChatGPT Codex (GPT-5.3-Codex)

## Profile
- **Strengths**: Agentic coding, multi-file refactoring, CI/CD pipelines, complex edits
- **Token Limit**: 128K tokens
- **Session Cost**: Medium (included in ChatGPT Plus £20/month)
- **Best For**: Large-scale refactors, CI/CD setup, cross-cutting changes
- **Agentic Mode**: Can propose and execute multi-step changes

---

## Current Sprint: Week 4 (Mar 17 - Mar 23, 2026)
**Theme**: Secure Transport + Device Enrollment

### Assigned Tasks

#### 1. CI/CD Pipeline Implementation
- [ ] **Full CI Workflow** (`.github/workflows/ci.yml`)
  - Lint: Python (ruff, black), JavaScript (eslint, prettier), YAML (yamllint)
  - Test: pytest (agent), jest (frontend), API integration tests
  - Security: bandit (Python SAST), npm audit, Trivy (container scan)
  - Coverage: Upload to Codecov, fail if <80%
  - Matrix: Test on Python 3.11, 3.12; Node 20, 22

- [ ] **Security Scan Workflow** (`.github/workflows/security-scan.yml`)
  - CodeQL: Analyze Python, JavaScript, Go
  - Dependency scan: Dependabot + Snyk
  - Secret scanning: TruffleHog, GitGuardian
  - Schedule: Daily at 2 AM UTC

- [ ] **Release Workflow** (`.github/workflows/release.yml`)
  - Trigger: Tag push (v*.*.*)
  - Build: Agent .deb package, Docker images (multi-arch: arm64, amd64)
  - SBOM: Generate with Syft (SPDX format)
  - Sign: Artifacts with cosign or GPG
  - Upload: GitHub Release, Docker Hub, Homebrew tap (future)
  - Changelog: Auto-generate from commits (conventional-changelog)

#### 2. Multi-File Refactoring
- [ ] **Standardize Error Handling**
  - Create: `agent/aetherpi_agent/exceptions.py` (custom exception classes)
  - Refactor: All collectors to use custom exceptions (not bare `Exception`)
  - Add: Error codes (e.g., `ERR_NMAP_FAILED`, `ERR_SCOPE_VIOLATION`)

- [ ] **Logging Standardization**
  - Create: `agent/aetherpi_agent/logging_config.py` (centralized logging setup)
  - Refactor: All modules to use structured logging (JSON format)
  - Add: Correlation IDs (trace requests across modules)

- [ ] **Type Annotations Enforcement**
  - Add: Type hints to all functions in `agent/aetherpi_agent/`
  - Configure: mypy strict mode
  - CI: Fail build on type errors

#### 3. Infrastructure as Code
- [ ] **Terraform Modules** (`infra/terraform/`)
  - AWS module: Deploy console (ECS Fargate, RDS PostgreSQL, ALB)
  - GCP module: Deploy console (Cloud Run, Cloud SQL, Load Balancer)
  - Variables: Region, instance size, backup retention

- [ ] **Ansible Playbooks** (`infra/ansible/`)
  - `deploy-agent.yml`: Install agent on multiple Pis
  - `update-agent.yml`: Rolling update across fleet
  - `collect-logs.yml`: Retrieve audit logs from agents

#### 4. WireGuard Automation
- [ ] **Key Management Scripts** (`infra/wireguard/`)
  - `generate-keys.sh`: Create server/client keypairs
  - `add-peer.sh`: Register new agent, update server config
  - `revoke-peer.sh`: Remove compromised agent
  - `rotate-keys.sh`: Periodic key rotation (automate with cron)

---

## Context

**Project State**:
- Week 3: Agent collectors implemented (Sonnet)
- Week 4: Add transport layer + enrollment
- Week 4 (your role): Set up CI/CD + infrastructure automation

**Your Mission**:
- Automate everything (testing, deployment, infrastructure)
- Enable one-command deployments
- Make CI/CD the "safety net" for other AIs' code

**Why You**:
- Agentic mode = propose multi-file changes, execute with approval
- Strong at DevOps/SRE tasks (CI/CD, IaC)
- Can handle complex GitHub Actions workflows

---

## Files to Create

```
.github/workflows/
├── ci.yml
├── security-scan.yml
└── release.yml

agent/aetherpi_agent/
├── exceptions.py
└── logging_config.py

infra/
├── terraform/
│   ├── aws/
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── gcp/
│       ├── main.tf
│       ├── variables.tf
│       └── outputs.tf
├── ansible/
│   ├── deploy-agent.yml
│   ├── update-agent.yml
│   └── collect-logs.yml
└── wireguard/
    ├── generate-keys.sh
    ├── add-peer.sh
    ├── revoke-peer.sh
    └── rotate-keys.sh
```

---

## Example: Release Workflow

```yaml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  build-agent:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build .deb package
        run: |
          cd agent
          python3 -m build
          # dpkg-deb commands here
      - name: Generate SBOM
        run: syft packages . -o spdx-json > sbom.json
      - name: Sign with cosign
        run: cosign sign-blob --key cosign.key agent.deb > agent.deb.sig
      - name: Upload to Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            agent.deb
            agent.deb.sig
            sbom.json
```

---

## Success Criteria

- [ ] All CI workflows pass on `main` branch
- [ ] Security scan finds no critical/high issues
- [ ] Release workflow creates GitHub Release with artifacts
- [ ] Terraform plans deploy successfully (test in staging)
- [ ] Ansible playbooks execute on test Pi fleet
- [ ] WireGuard scripts tested with 3+ peers

---

## Constraints

**Token Budget**:
- This sprint: ~100K tokens (CI/CD + IaC + refactors)
- Agentic mode: Propose changes, get approval, execute

**Time Estimate**:
- 10-15 hours (can span multiple days)

**Dependencies**:
- Agent code (Sonnet, Week 3)
- Docker configs (Haiku, Week 1)

---

## Blockers

None currently.

---

## Notes for Next Session (Week 7)

**Future Tasks**:
- Week 7: Implement E2E test harness
- Add: Chaos engineering tests (agent failure scenarios)
- Optimize: CI runtime (caching, parallelization)

---

## Handoff to Other AIs

**After completing this sprint**:

→ **Human maintainer**: Configure GitHub secrets (API keys, signing keys)  
→ **Haiku**: Update Dockerfiles based on CI findings  
→ **Sonnet**: Fix any bugs found by security scans  

---

**Status**: 🔵 QUEUED (starts Mar 17)  
**Last Updated**: February 24, 2026  
**Next Review**: March 23, 2026
