# ADR-0003: Data Serialization Format

**Status**: Accepted  
**Date**: 2026-02-24  
**Deciders**: @zebadee2kk  

---

## Context

KYNEĒ components (agent, console, AI module) exchange structured data:

- **Findings**: Vulnerability reports, network inventory
- **Audit Logs**: Immutable records of all actions
- **Job Dispatch**: Commands from console to agent
- **Agent Status**: Heartbeats, health metrics

Data must be:

1. **Human-readable** (for debugging, legal review)
2. **Machine-parseable** (automated processing)
3. **Schema-validated** (prevent malformed data)
4. **Language-agnostic** (Python agent, Python/JS console, future Go rewrite)
5. **Efficient** (Pi 3 has limited resources)

**Options Considered**:

### Option 1: JSON

- ✅ Human-readable
- ✅ Universal support (Python `json`, JS native, Go `encoding/json`)
- ✅ Schema validation (JSON Schema)
- ✅ Debuggable (can inspect with `jq`, text editors)
- ⚠️ Larger payload than binary formats (~30% overhead)
- ⚠️ No native timestamp/date types

### Option 2: Protocol Buffers (protobuf)

- ✅ Compact binary format
- ✅ Fast serialization
- ✅ Schema enforcement (`.proto` files)
- ⚠️ Not human-readable (requires `protoc` to inspect)
- ⚠️ Requires code generation step
- ⚠️ Harder to debug

### Option 3: MessagePack

- ✅ Binary JSON (smaller than JSON, larger than protobuf)
- ✅ Faster than JSON
- ⚠️ Less tooling support
- ⚠️ Not human-readable

### Option 4: YAML

- ✅ Human-readable
- ✅ Supports comments
- ⚠️ Slower parsing than JSON
- ⚠️ Whitespace-sensitive (error-prone)
- ⚠️ Security issues (arbitrary code execution in some parsers)

### Option 5: CBOR (Concise Binary Object Representation)

- ✅ Compact
- ✅ RFC 8949 standard
- ⚠️ Less adoption than JSON/protobuf
- ⚠️ Not human-readable

---

## Decision

**We will use JSON with JSON Schema validation.**

### Rationale

1. **Human-Readability Priority**
   - Legal/compliance requirement: Audit logs must be inspectable by non-technical auditors
   - Debugging: Operators can `cat findings.json` without special tools
   - Transparency: Clients can review raw data

2. **Ecosystem Maturity**
   - Every language has robust JSON support
   - JSON Schema provides strong validation (types, required fields, enums)
   - Tooling: `jq`, `jsonlint`, IDE support

3. **Performance Acceptable**
   - Findings are small (<10KB per scan result)
   - Network bandwidth is not a bottleneck (WireGuard VPN or LAN)
   - Compression (gzip) reduces size by ~70% if needed

4. **Future-Proofing**
   - Allows rewriting components in different languages
   - JSON is lingua franca of APIs

### Performance Mitigation

- Use `ujson` or `orjson` (10x faster than stdlib `json`)
- Enable gzip compression for large payloads (>1KB)
- Stream large datasets (JSONL - JSON Lines format)

---

## Implementation

### JSON Schema Definitions

**Location**: `schemas/*.schema.json`

**Example** (`schemas/findings.schema.json`):
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://kynee.dev/schemas/findings.schema.json",
  "title": "KYNEĒ Findings",
  "type": "object",
  "properties": {
    "engagement_id": { "type": "string", "format": "uuid" },
    "agent_id": { "type": "string", "format": "uuid" },
    "timestamp": { "type": "string", "format": "date-time" },
    "tool": { "type": "string" },
    "category": { "type": "string", "enum": ["network", "wireless", "bluetooth", "physical", "credential"] },
    "severity": { "type": "string", "enum": ["informational", "low", "medium", "high", "critical"] },
    "description": { "type": "string" },
    "evidence": { "type": "object" }
  },
  "required": ["engagement_id", "agent_id", "timestamp", "tool", "category", "severity", "description"]
}
```

### Validation

**Python** (agent, console backend):
```python
import jsonschema
import json

with open('schemas/findings.schema.json') as f:
    schema = json.load(f)

data = { ... }  # Findings object
jsonschema.validate(instance=data, schema=schema)
```

**JavaScript** (console frontend):
```javascript
import Ajv from 'ajv';
import schema from './schemas/findings.schema.json';

const ajv = new Ajv();
const validate = ajv.compile(schema);
const valid = validate(data);
if (!valid) console.error(validate.errors);
```

### File Formats

**Single Object**: `.json`
```json
{ "engagement_id": "...", "findings": [...] }
```

**Stream of Objects**: `.jsonl` (JSON Lines)
```json
{"timestamp": "...", "event": "scan_start"}
{"timestamp": "...", "event": "finding", "severity": "high"}
{"timestamp": "...", "event": "scan_complete"}
```

**When to use JSONL**:
- Audit logs (append-only)
- Streaming findings (real-time ingestion)

---

## Consequences

### Positive

- ✅ Maximum transparency (human + machine readable)
- ✅ Strong ecosystem (libraries, tooling)
- ✅ Easy debugging (text editors, `jq`)
- ✅ Legal compliance (auditable plaintext)
- ✅ Language-agnostic (future rewrites possible)

### Negative

- ⚠️ Larger payloads than binary formats (~30% overhead)
- ⚠️ Slower parsing than protobuf (~2-5x)
- ⚠️ No native binary data (must base64-encode)

### Mitigations

- Use fast JSON libraries (`orjson`, `ujson`)
- Enable gzip compression for network transport
- Profile and optimize if performance becomes an issue

### Trade-Offs Accepted

- We prioritize **transparency** and **debuggability** over raw performance
- For a penetration testing tool, human inspectability is critical
- Pi 3 can handle JSON parsing for expected workloads (<1000 findings/hour)

---

## Future Considerations

### If Performance Becomes Critical

1. **Add protobuf as optional transport**:
   - JSON for storage/debugging
   - Protobuf for agent ↔ console communication
   - Conversion layer in console

2. **Compression**:
   - Enable gzip for all API responses
   - Use zstd for long-term log storage

3. **Chunking**:
   - Split large findings into smaller batches
   - Stream via JSONL

---

## Related Decisions

- [ADR-0002: Transport Protocol](adr-0002-transport-protocol.md) (JSON over WireGuard/HTTPS)
- [ADR-0004: Audit Log Immutability](adr-0004-audit-log-immutability.md) (JSONL format for logs)

---

**Last Updated**: February 24, 2026  
**Maintained By**: @zebadee2kk
