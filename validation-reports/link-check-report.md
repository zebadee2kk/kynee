# Link Check Report

- Tool: `markdown-link-check`
- Status: **PASS WITH WARNINGS**

## Summary
- Broken links detected (total events): 59
- Main categories:
  - Missing local files (planned-but-not-yet-created docs)
  - GitHub Discussions URL returns 404
  - Some third-party external docs returning 403/404/503
  - `mailto:` marked as invalid by checker configuration

## High-signal broken internal links
- `CONTRIBUTING.md` → `CONTRIBUTORS.md`
- `SECURITY.md` → `docs/build/hardening-baseline.md`
- `SECURITY.md` → `docs/security-hall-of-fame.md`
- `SECURITY.md` → `docs/ops/incident-response.md`
- `SUPPORT.md` → `docs/build/kali-rpi3-minimal.md`

Raw output: `validation-reports/raw/linkcheck.txt`.
