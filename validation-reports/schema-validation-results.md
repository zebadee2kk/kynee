# Schema Validation Results

- Validator: `ajv-cli` with Draft 2020-12 + `ajv-formats`
- Status: **PASS**

## Compile Results
- `schemas/findings.schema.json`: ✅ valid
- `schemas/inventory.schema.json`: ✅ valid
- `schemas/auditlog.schema.json`: ✅ valid
- `schemas/agent-status.schema.json`: ✅ valid

## Sample Data Validation
- Valid samples: **12/12 passed**
- Invalid samples: **12/12 correctly rejected**

See raw logs in `validation-reports/raw/*.compile.txt` and `validation-reports/raw/sample-validation.txt`.
