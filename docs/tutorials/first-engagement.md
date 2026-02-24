# Tutorial: Your First KYNEE Engagement

This walkthrough shows a safe, end-to-end flow for a basic authorized engagement.

**Important:** Only run KYNEE on systems you have explicit written authorization to test. Use the Rules of Engagement (RoE) template: [docs/legal/rules-of-engagement-template.md](../legal/rules-of-engagement-template.md).

---

## Before You Begin

- KYNEE console running (local or hosted)
- Agent installed on a Raspberry Pi
- An RoE document signed by the client
- A clearly defined scope (CIDR ranges, domains, and physical locations)

---

## Step 1: Create an Engagement

1. Log in to the console.
2. Select **Engagements** -> **New Engagement**.
3. Enter a name, client, and dates.
4. Upload the signed RoE.

**Tip:** Put the key scope constraints in the engagement notes so operators see them before running actions.

---

## Step 2: Define Scope

Add only in-scope assets. Example:

- `10.0.5.0/24`
- `app.client-domain.net`
- Physical: Building A, Floor 2

**Warning:** Do not include production systems or third-party services unless the RoE explicitly permits it.

---

## Step 3: Enroll the Agent

1. In the console, create an enrollment token.
2. On the Raspberry Pi:

```bash
sudo kynee-agent enroll --console https://console.example.com --token <TOKEN>
```

3. Confirm the agent appears under **Devices**.

---

## Step 4: Start a Scan

1. Open the engagement.
2. Choose the data collection modules (network, wireless, bluetooth).
3. Set a schedule or start immediately.
4. Confirm the console shows **In Progress**.

---

## Step 5: Review Findings

1. Go to **Findings**.
2. Filter by severity and asset.
3. Review evidence and affected systems.

If you see a critical issue, follow your escalation procedures in the RoE.

---

## Step 6: Export a Report

1. Open the engagement summary.
2. Select **Export Report** (Markdown or PDF).
3. Store the report per your data handling requirements.

---

## Step 7: Close the Engagement

1. Stop scheduled jobs.
2. Disable the agent for the engagement.
3. Archive the RoE and audit logs.

---

## What to Do If You Accidentally Scan Out of Scope

1. Stop all scans immediately.
2. Notify the client point of contact.
3. Record the incident in the audit log.
4. Follow the RoE incident response section.

---

## Next Steps

- Read [Tutorial: Interpreting Findings](interpreting-findings.md)
- Review the security model: [docs/security-model.md](../security-model.md)
