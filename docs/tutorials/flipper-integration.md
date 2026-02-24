# Tutorial: Integrating Flipper Zero

This guide shows how to connect a Flipper Zero to KYNEE for authorized physical-layer testing.

**Important:** Physical testing requires explicit RoE approval. Do not proceed without written authorization.

---

## Before You Begin

- Flipper Zero with firmware v0.80.0+
- USB-C to USB-A cable
- Raspberry Pi running the KYNEE agent
- RoE includes physical testing scope

See [hardware/flipper/integration-notes.md](../../hardware/flipper/integration-notes.md) for wiring details.

---

## Step 1: Connect the Flipper

1. Power on the Flipper Zero.
2. Connect it to the Pi using USB.
3. Verify it appears as a serial device:

```bash
ls -l /dev/ttyACM*
```

You should see `/dev/ttyACM0`.

---

## Step 2: Install Python Dependencies

```bash
pip install pyserial
```

---

## Step 3: Enable Flipper Actions for the Engagement

1. In the console, open the engagement settings.
2. Enable **Flipper Zero Actions**.
3. Add a justification note that references the RoE section.

---

## Step 4: Run a Test Command

On the agent:

```bash
python - << 'PY'
import serial

flipper = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
flipper.write(b'help\r\n')
print(flipper.read(1024).decode())
flipper.close()
PY
```

If the CLI responds, the connection is ready.

---

## Step 5: Review Findings and Logs

- Findings should appear in the console.
- Audit logs should include the command, operator, and RoE reference.

---

## Safety Rules

- Never emulate or transmit signals without explicit approval.
- Avoid any action that could cause physical harm or service disruption.
- Disable Flipper actions when the engagement ends.

---

## Troubleshooting

**No `/dev/ttyACM0` found**
- Reconnect the cable and power-cycle the Flipper.
- Load the `cdc_acm` module:

```bash
sudo modprobe cdc_acm
```

**Permission denied**
- Add your user to `dialout` and re-login:

```bash
sudo usermod -a -G dialout $USER
```

---

## Next Steps

- Review the full engagement flow: [docs/tutorials/first-engagement.md](first-engagement.md)
- Understand audit logging: [docs/security-model.md](../security-model.md)
