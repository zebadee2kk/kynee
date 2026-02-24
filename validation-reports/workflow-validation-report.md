# Workflow Validation Report

- Tools: `actionlint`, `yamllint`
- Status: **PASS**

## Results
- `.github/workflows/ci.yml`: ✅ valid
- `.github/workflows/security-scan.yml`: ✅ valid

## Fixes applied during validation
- Added YAML document start (`---`) and quoted `'on'` key for lint compatibility.
- Updated security scan schedule from weekly to daily at `02:00 UTC`.
- Added Go to CodeQL language list (`python, javascript, go`).
- Fixed style/lint issues in workflow YAML.

Raw output: `validation-reports/raw/actionlint.txt` and `validation-reports/raw/yamllint.txt`.
