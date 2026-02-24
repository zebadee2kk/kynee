# AI Assistant Behavior

The KYNEE AI assistant analyzes findings and suggests next steps. It never executes actions directly.

---

## What the AI Uses

- Findings and metadata (severity, asset, evidence)
- Engagement scope (allowlists, time windows)
- RoE references and constraints
- Operator feedback history

---

## Output Format (Conceptual)

The assistant returns structured proposals for review:

```json
{
  "suggestion_id": "SUG-2026-0001",
  "summary": "Validate SMBv1 exposure on 10.0.5.12",
  "justification": "Finding F-102 indicates SMBv1 enabled; in scope",
  "recommended_action": "run_nmap_smb_protocols",
  "parameters": {
    "target": "10.0.5.12"
  },
  "risk": "low",
  "roe_reference": "Section 5: Permitted Techniques"
}
```

---

## Guardrails

- **No autonomous actions**: Suggestions require approval.
- **Scope-aware**: Out-of-scope targets are rejected.
- **RoE-aware**: Actions must map to permitted methods.
- **Conservative defaults**: Prefer validation and low-risk checks.

---

## Approval Workflow

1. AI generates 3-5 suggestions from current findings.
2. Operator approves, rejects, or edits each suggestion.
3. Approved actions are logged with an operator ID and reason.
4. Results feed back into the findings list.

---

## Example Suggested Actions

- Validate a suspected service exposure
- Perform a safe version check on an in-scope host
- Request a targeted wireless scan within a time window

---

## Failure Modes

- Hallucinated tools or commands
- Recommendations that are too aggressive
- Missing RoE citations

Operators must review all suggestions before approving.
