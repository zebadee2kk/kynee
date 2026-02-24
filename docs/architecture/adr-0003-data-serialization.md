# ADR-0003: Data Serialization Format

**Status**: Proposed  
**Date**: 2026-02-24  
**Deciders**: @zebadee2kk, Architecture Team  
**Technical Story**: Week 1 roadmap milestone

---

## Context

The agent and console exchange structured data:

- **Findings**: Security vulnerabilities and observations
- **Inventory**: Discovered assets (hosts, wireless APs, Bluetooth devices)
- **Audit Logs**: Immutable record of all actions
- **Agent Status**: Heartbeats and health metrics

We need a serialization format that is:

- **Human-readable**: Easy to debug and inspect
- **Schema-validated**: Prevent malformed data
- **Language-agnostic**: Works with Python (agent), JavaScript (console frontend), any future languages
- **Efficient**: Low overhead for Pi 3
- **Versioned**: Support schema evolution

---

## Decision

**Use JSON with JSON Schema validation.**

### Rationale

1. **Ubiquity**: Native support in Python (`json`), JavaScript, every language
2. **Human-readable**: Easy to inspect in logs, debug with `jq`
3. **Tooling**: JSON Schema provides validation, documentation generation
4. **Flexibility**: Easy to evolve schemas (add optional fields)
5. **Ecosystem**: Rich tooling (validators, linters, editors)

---

## Consequences

### Positive

- **Zero learning curve**: Everyone knows JSON
- **Debugging**: Can inspect messages in plaintext (after decryption)
- **Schema evolution**: JSON Schema supports optional fields, defaults
- **Interoperability**: Works with any language/tool

### Negative

- **Larger payload**: More verbose than binary formats (Protobuf, MessagePack)
- **No built-in versioning**: Must track schema versions manually
- **Type safety**: Requires runtime validation (no compile-time checks)

### Neutral

- Compress JSON with gzip for transport (WireGuard/HTTPS)
- Use JSON Schema `$schema` and `$id` for version tracking
- Validate all messages on ingestion (agent and console)

---

## Alternatives Considered

### Alternative 1: Protocol Buffers (Protobuf)

**Pros**:
- Compact binary format (~3x smaller than JSON)
- Strongly typed, compile-time validation
- Schema evolution built-in
- Fast serialization/deserialization

**Cons**:
- Not human-readable (requires `protoc` to inspect)
- Requires code generation (`.proto` → Python/JS)
- Harder to debug
- Overhead for small messages

**Why Rejected**: Human-readability and debugging are priorities; compression mitigates size difference.

### Alternative 2: MessagePack

**Pros**:
- Binary format, smaller than JSON
- Faster than JSON parsing
- Drop-in JSON replacement

**Cons**:
- Not human-readable
- Less tooling than JSON
- No built-in schema validation

**Why Rejected**: Minimal performance gain not worth loss of human-readability.

### Alternative 3: YAML

**Pros**:
- Human-readable
- Supports comments
- More concise than JSON

**Cons**:
- Parsing ambiguities (security issues)
- Slower parsing than JSON
- Less ubiquitous in APIs

**Why Rejected**: YAML parsing vulnerabilities (Norway problem, arbitrary code execution); JSON is safer.

---

## Implementation Notes

### Schema Storage

All schemas stored in `schemas/*.schema.json`:

- `findings.schema.json`
- `inventory.schema.json`
- `auditlog.schema.json`
- `agent-status.schema.json`

### Validation

**Agent** (Python):
```python
import jsonschema
import json

with open('schemas/findings.schema.json') as f:
    schema = json.load(f)

finding = {...}  # Data to validate
jsonschema.validate(finding, schema)  # Raises exception if invalid
```

**Console Backend** (Python/FastAPI):
```python
from pydantic import BaseModel, Field

class Finding(BaseModel):
    finding_id: str = Field(..., regex=r'^[0-9a-f-]{36}$')
    engagement_id: str
    severity: str = Field(..., regex=r'^(informational|low|medium|high|critical)$')
    # ...
```

**Console Frontend** (TypeScript):
```typescript
import Ajv from 'ajv';
import findingSchema from '@/schemas/findings.schema.json';

const ajv = new Ajv();
const validate = ajv.compile(findingSchema);

if (!validate(finding)) {
  console.error(validate.errors);
}
```

### Versioning Strategy

Each schema includes version in `$id`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://kynee.dev/schemas/findings.schema.json",
  "version": "1.0.0"
}
```

Breaking changes increment major version:

- `findings.v1.schema.json`
- `findings.v2.schema.json`

Console supports multiple schema versions during transition period.

---

## Performance Considerations

- **Compression**: gzip reduces JSON size by ~70%
- **Streaming**: Use `ijson` (Python) for large payloads
- **Caching**: Validate schema once, reuse validator

---

## References

- [JSON Schema Specification](https://json-schema.org/)
- [JSON vs. Protobuf Benchmarks](https://github.com/eishay/jvm-serializers/wiki)
- [JSON Security Best Practices](https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_for_Java_Cheat_Sheet.html)

---

**Last Updated**: February 24, 2026  
**Status**: Proposed (requires maintainer approval)
