# ADR-0003: Data Serialization Format

## Status
**Accepted** (2026-02-24)

## Context

KYNEĒ agents generate structured data (findings, inventory, audit logs) that must be:

- **Validated**: Conform to schemas for consistency.
- **Transmittable**: Sent over network efficiently.
- **Stored**: Persisted in console database.
- **Human-readable**: For debugging and report generation.
- **Extensible**: Allow new fields without breaking old parsers.

**Options Considered**:

1. **JSON**
   - Pros: Universal, human-readable, rich tooling, native browser support
   - Cons: Verbose, no built-in schema enforcement, no binary efficiency

2. **Protocol Buffers (protobuf)**
   - Pros: Compact, fast, strong typing, backward-compatible
   - Cons: Not human-readable, requires .proto files, compile step

3. **MessagePack**
   - Pros: Binary JSON, smaller than JSON, fast
   - Cons: Less tooling, not human-readable, schema enforcement manual

4. **YAML**
   - Pros: Human-readable, supports comments
   - Cons: Slow parsing, security issues (arbitrary code execution), no schema enforcement

## Decision

**JSON with JSON Schema validation**.

### Rationale

1. **Ubiquity**: Every language, tool, and browser supports JSON natively.
2. **Human-Readable**: Operators can inspect findings in text editors, logs, or CLI (`jq`).
3. **Schema Validation**: JSON Schema (draft 2020-12) provides strong typing, required fields, enums, and formats.
4. **Tooling**: Rich ecosystem (`jsonschema` in Python, Ajv in JS, online validators).
5. **Extensibility**: JSON Schema supports `additionalProperties: false` for strict validation, or `true` for forward compatibility.
6. **Debugging**: Easy to log, inspect, and diff JSON during development.

### Schema Location

All schemas stored in `schemas/*.schema.json`:

- `findings.schema.json`
- `inventory.schema.json`
- `auditlog.schema.json`
- `agent-status.schema.json`

### Validation

- **Agent**: Validates output before transmission (fail-fast on schema violations).
- **Console**: Validates input on API ingestion (reject malformed data).
- **CI**: Schema validation tests in test suite.

## Consequences

### Positive

- **Interoperability**: Any tool can consume KYNEĒ data (Splunk, ELK, custom scripts).
- **Auditability**: JSON logs are grep-able, jq-able, and archivable.
- **Validation**: JSON Schema catches data errors early (e.g., missing `engagement_id`).
- **Documentation**: Schemas self-document data structure.

### Negative

- **Verbosity**: JSON is ~30% larger than MessagePack, ~50% larger than protobuf.
- **Performance**: Parsing JSON is slower than binary formats (acceptable for our scale).
- **Schema Drift**: Manual discipline required to keep schemas in sync with code.

### Neutral

- JSON Schema is evolving (draft 2020-12 is current), but backward-compatible.

## Implementation Details

### Example: Findings Output (Agent)

```python
import json
from jsonschema import validate

finding = {
    "engagement_id": "ENG-2026-042",
    "agent_id": "550e8400-e29b-41d4-a716-446655440000",
    "finding_id": "f1234567-89ab-cdef-0123-456789abcdef",
    "timestamp": "2026-03-15T14:32:01Z",
    "tool": "nmap",
    "category": "vulnerability",
    "severity": "high",
    "title": "SSH weak key exchange algorithms",
    "description": "Server supports deprecated KEX algorithms",
    "target": {
        "ip_address": "10.0.5.42",
        "port": 22,
        "protocol": "tcp",
        "service": "ssh"
    }
}

with open("schemas/findings.schema.json") as f:
    schema = json.load(f)

validate(instance=finding, schema=schema)  # Raises exception if invalid
print(json.dumps(finding, indent=2))
```

### Example: Validation (Console API)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import jsonschema

app = FastAPI()

class Finding(BaseModel):
    engagement_id: str = Field(..., pattern=r"^ENG-[0-9]{4}-[0-9]{3}$")
    agent_id: str = Field(..., format="uuid")
    # ... other fields

@app.post("/api/v1/findings")
async def ingest_finding(finding: Finding):
    # Pydantic validates automatically
    # Additional JSON Schema validation if needed
    return {"status": "accepted", "finding_id": finding.finding_id}
```

## Alternatives Revisited

- **If bandwidth becomes critical**: Compress JSON with gzip (reduces size ~70%), or use MessagePack for transport + JSON for storage.
- **If protobuf adoption grows**: Consider hybrid (protobuf for transport, JSON for storage), but adds complexity.

---

**Decision Maker**: @zebadee2kk  
**Date**: February 24, 2026  
**Supersedes**: None
