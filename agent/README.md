# KYNEE Agent

The KYNEE agent runs on a Raspberry Pi and performs authorized data collection during a security assessment. It reports findings back to the console and records immutable audit logs.

**Important:** Use only with written authorization. See [ETHICAL_USE_POLICY.md](../ETHICAL_USE_POLICY.md).

---

## Hardware Requirements

- Raspberry Pi 3 Model B+ or better
- 32GB+ microSD (Class 10 or better)
- Optional Wi-Fi and Bluetooth adapters for advanced testing

For recommended hardware, see [hardware/bill-of-materials.md](../hardware/bill-of-materials.md).

---

## OS Requirements

- Kali Linux ARM (2024.1+)

---

## Installation (Coming Soon)

Packaging is planned for Week 7. Until then, the agent can be run from source when the core code lands (Week 3-4).

```bash
# Placeholder - exact steps will be added when packaging is available
sudo dpkg -i kynee-agent_0.9.0_armhf.deb
```

---

## Configuration

Planned default configuration location:

```
/etc/kynee/agent.yaml
```

Expected configuration keys (subject to change):
- `console_url`: Console endpoint (HTTPS or WireGuard)
- `enrollment_token`: One-time token for pairing
- `scan_schedule`: Cron-like schedule for collectors
- `scope_allowlist`: CIDR ranges and hostnames in scope

---

## Service Management

The agent will run as a systemd service.

```bash
sudo systemctl enable kynee-agent
sudo systemctl start kynee-agent
sudo systemctl status kynee-agent
```

---

## Logs and Data

Planned locations:

- Audit log: `/var/lib/kynee/audit.log`
- Findings cache: `/var/lib/kynee/findings/`
- Agent log: `/var/log/kynee/agent.log`

---

## Verification Checks

Run basic checks to confirm hardware and OS readiness:

```bash
# CPU / memory
uname -a
free -h

# Wi-Fi
iwconfig

# Bluetooth
hciconfig

# USB devices
lsusb
```

---

## Uninstall (When Packaged)

```bash
sudo dpkg -r kynee-agent
```

---

## Security and Ethics

- Do not scan out-of-scope systems.
- Keep the Rules of Engagement (RoE) attached to each engagement.
- Ensure logs are preserved for auditability.

---

## Status

The agent is in **pre-alpha**. Expect breaking changes as core collectors and transport layers are implemented.
