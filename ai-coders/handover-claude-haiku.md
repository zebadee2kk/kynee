# Handover: Claude Haiku

## Profile
- **Strengths**: Fast responses, simple tasks, config files, boilerplate code
- **Token Limit**: 200K tokens
- **Session Cost**: Low (API pricing, ~£/1M tokens)
- **Best For**: YAML/JSON configs, Dockerfiles, shell scripts, data fixtures

---

## Current Sprint: Week 1 (Feb 24 - Mar 2, 2026)
**Theme**: Foundations + Governance

### Assigned Tasks

#### 1. JSON Schemas
Create schema files for data validation:

- [ ] **Findings Schema** (`schemas/findings.schema.json`)
  - Network scan results (nmap, airodump, hcitool)
  - Fields: finding_id, timestamp, engagement_id, type, severity, target, details
  - Nested objects for ports, services, wireless APs

- [ ] **Inventory Schema** (`schemas/inventory.schema.json`)
  - Asset tracking (hosts, devices, networks)
  - Fields: asset_id, first_seen, last_seen, mac, ip, hostname, os

- [ ] **Audit Log Schema** (`schemas/auditlog.schema.json`)
  - Immutable event log
  - Fields: timestamp, engagement_id, operator_id, action, target, outcome, previous_hash

- [ ] **Agent Status Schema** (`schemas/agent-status.schema.json`)
  - Device health (CPU, memory, disk, uptime)
  - Last heartbeat, connectivity status

#### 2. Configuration Templates
- [ ] **Agent Config** (`agent/config.example.yaml`)
  - Scope (allowed_networks, denied_networks)
  - Collectors (enabled_modules, scan_intervals)
  - Transport (wireguard_config, console_api_url)
  - Audit log path

- [ ] **Console Config** (`console/backend/config.example.yaml`)
  - Database connection (PostgreSQL)
  - JWT secret (placeholder with warning)
  - AI backend (Ollama URL or OpenAI API key)
  - File upload limits

#### 3. Docker Configs
- [ ] **Agent Dockerfile** (`agent/Dockerfile`)
  - Base: Kali Linux ARM or Debian with security tools
  - Install: Python 3.11, nmap, aircrack-ng, bluez
  - Copy agent code, set entrypoint

- [ ] **Console Backend Dockerfile** (`console/backend/Dockerfile`)
  - Base: Python 3.11-slim
  - Install: FastAPI, SQLAlchemy, psycopg2
  - Multi-stage build (smaller image)

- [ ] **Console Frontend Dockerfile** (`console/frontend/Dockerfile`)
  - Base: Node 20
  - Build React app, serve with nginx

- [ ] **docker-compose.yml** (root)
  - Services: postgres, console-backend, console-frontend
  - Volumes, networks, environment variables

#### 4. Shell Scripts
- [ ] **Image Build Script** (`scripts/image-build/build-kali-minimal.sh`)
  - Download Kali ARM image
  - Mount, chroot, customize (remove unnecessary packages)
  - Install agent dependencies
  - Compress and hash final image

- [ ] **Provisioning Script** (`scripts/provisioning/first-boot.sh`)
  - Run on first Pi boot
  - Create `aetherpi` user
  - Generate SSH keys
  - Expand filesystem
  - Set timezone, hostname

- [ ] **Enrollment Script** (`scripts/provisioning/enroll-device.sh`)
  - Interactive: prompt for console URL, enrollment token
  - Generate device keys (WireGuard)
  - Register with console API
  - Save config to `/etc/aetherpi/agent.yaml`

#### 5. CI/CD Workflow Skeleton
- [ ] **Lint & Test** (`.github/workflows/ci.yml`)
  - Trigger: on push, pull request
  - Jobs: lint (Python, JS), test (pytest, jest), security scan

- [ ] **Release** (`.github/workflows/release.yml`)
  - Trigger: on tag push (v*.*.*)
  - Build: agent .deb, Docker images
  - Generate: SBOM, checksums
  - Upload: GitHub Release, Docker Hub

---

## Context

**Project State**:
- Repository initialized, governance docs complete
- Week 1: Create foundational configs and schemas
- Other AIs depend on your schemas for validation

**Your Mission**:
- Generate all boilerplate configs and schemas
- Make them copy-paste ready (no TODOs, use sensible defaults)
- Fast turnaround (you're the project's "template factory")

**Why You**:
- Low cost = high volume of simple tasks
- Fast responses minimize iteration time
- Perfect for structured data (JSON, YAML)

---

## Files to Create

```
schemas/
├── findings.schema.json
├── inventory.schema.json
├── auditlog.schema.json
└── agent-status.schema.json

agent/
├── config.example.yaml
└── Dockerfile

console/backend/
└── config.example.yaml

console/backend/
└── Dockerfile

console/frontend/
└── Dockerfile

docker-compose.yml

scripts/image-build/
└── build-kali-minimal.sh

scripts/provisioning/
├── first-boot.sh
└── enroll-device.sh

.github/workflows/
├── ci.yml
└── release.yml
```

---

## Example: Findings Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Security Finding",
  "type": "object",
  "required": ["finding_id", "timestamp", "engagement_id", "type", "target"],
  "properties": {
    "finding_id": {
      "type": "string",
      "format": "uuid"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "engagement_id": {
      "type": "string"
    },
    "type": {
      "type": "string",
      "enum": ["network_scan", "wireless_scan", "bluetooth_scan", "vulnerability"]
    },
    "severity": {
      "type": "string",
      "enum": ["critical", "high", "medium", "low", "info"]
    },
    "target": {
      "type": "string"
    },
    "details": {
      "type": "object"
    }
  }
}
```

---

## Success Criteria

- [ ] All 4 JSON schemas validate with `ajv` or `jsonschema`
- [ ] Config files have sensible defaults (no empty placeholders)
- [ ] Dockerfiles build successfully (`docker build -t test .`)
- [ ] Shell scripts are executable and have proper shebangs (`#!/usr/bin/env bash`)
- [ ] CI workflows syntax-check with `actionlint`

---

## Constraints

**Token Budget**:
- Total: ~20K tokens (all tasks are short)
- Single session sufficient

**Time Estimate**:
- 1-2 hours

**Dependencies**:
- None (Week 1 is foundational)

---

## Blockers

None currently.

---

## Notes for Future Sprints

**Recurring Tasks** (every 2-3 weeks):
- Update schemas as new finding types added
- Generate new config templates for features
- Create deployment scripts (Ansible, Terraform)

**When to Call Haiku**:
- "We need a config file for X"
- "Generate a Dockerfile for Y"
- "Create a bash script to Z"
- "Mock data for testing"

---

## Handoff to Other AIs

**After completing this sprint**:

→ **Claude Sonnet**: Use schemas for validation in agent collectors  
→ **Codex**: Reference Dockerfiles when setting up CI/CD  
→ **ChatGPT**: Document config options in user guide  

---

**Status**: 🟢 READY TO START  
**Last Updated**: February 24, 2026  
**Next Review**: March 2, 2026
