# Flipper Zero Integration Notes

## Overview

The Flipper Zero is a portable multi-tool for security research, capable of interacting with:
- **RFID** (125 kHz Low Frequency)
- **NFC** (13.56 MHz High Frequency)
- **Sub-GHz** (433/868/915 MHz)
- **Infrared** (IR remote controls)
- **GPIO** (hardware hacking, UART, SPI, I2C)
- **USB** (BadUSB, keyboard emulation)

KYNEĒ integrates Flipper Zero to extend physical-layer testing capabilities during authorized penetration tests.

---

## Connection Methods

### Method 1: USB (Serial) — Recommended

**Hardware**:
- USB-C to USB-A cable
- Raspberry Pi 3 USB port

**Interface**:
- Device appears as `/dev/ttyACM0` (serial console)
- Baud rate: 115200
- Protocol: Flipper CLI commands

**Advantages**:
- Simple setup (plug-and-play)
- Stable communication
- Powers Flipper from Pi (if sufficient power)

**Disadvantages**:
- Occupies a USB port (Pi 3 only has 4)
- Flipper must be physically connected

**Python Library**: `flipperzero-py` or `pyserial`

```python
import serial

flipper = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
flipper.write(b'help\r\n')
print(flipper.read(1024).decode())
```

---

### Method 2: UART (GPIO) — Advanced

**Hardware**:
- Flipper Zero GPIO pins (accessible via 18-pin header)
- Raspberry Pi GPIO pins
- Jumper wires (female-to-female)

**Pinout**:

| Flipper Zero Pin | Function | Raspberry Pi Pin | GPIO Number |
|------------------|----------|------------------|-------------|
| Pin 13 | TX (transmit) | Pin 10 | GPIO 15 (RXD) |
| Pin 14 | RX (receive) | Pin 8 | GPIO 14 (TXD) |
| Pin 18 | GND (ground) | Pin 6 | GND |

**Wiring Diagram**:
```
Flipper Zero (GPIO)           Raspberry Pi 3 (GPIO)
┌─────────────────┐       ┌─────────────────┐
│ Pin 13 (TX)    ├───────├─────▶ GPIO 15 (RX)  │
│ Pin 14 (RX)    ├───────├─────◀ GPIO 14 (TX)  │
│ Pin 18 (GND)   ├───────├─────▶ GND           │
└─────────────────┘       └─────────────────┘
```

**Configuration** (`/boot/config.txt`):
```ini
enable_uart=1
```

**Disable Serial Console** (to free `/dev/ttyS0`):
```bash
sudo raspi-config
# Interface Options → Serial Port → Disable shell, Enable hardware
```

**Python Library**: `pyserial`

```python
import serial

flipper = serial.Serial('/dev/ttyS0', 115200, timeout=1)
flipper.write(b'help\r\n')
print(flipper.read(1024).decode())
```

**Advantages**:
- Frees up USB ports
- More compact wiring (can be internal to enclosure)

**Disadvantages**:
- Requires custom cable/soldering
- Flipper must be powered separately

---

## Flipper CLI Commands

### RFID (125 kHz Low Frequency)

**Read Card**:
```
rfid read
```

**Emulate Card**:
```
rfid emulate <file.rfid>
```

**Example Output**:
```
RFID 125kHz:
HID ProxCard II
FC: 123, Card: 45678
```

---

### NFC (13.56 MHz High Frequency)

**Scan NFC Tag**:
```
nfc detect
```

**Read NFC Tag**:
```
nfc read
```

**Emulate NFC Tag**:
```
nfc emulate <file.nfc>
```

**Example Output**:
```
NFC:
MIFARE Classic 1K
UID: 04 A1 B2 C3 D4 E5 F6
SAK: 08, ATQA: 00 04
```

---

### Sub-GHz (433/868/915 MHz)

**Scan Frequencies**:
```
subghz rx
```

**Read Remote**:
```
subghz read
```

**Transmit Signal**:
```
subghz tx <file.sub>
```

**Example Output**:
```
Sub-GHz:
Frequency: 433.92 MHz
Protocol: Princeton (PT-2262)
Key: 0x123456
```

---

### Infrared (IR)

**Learn Remote**:
```
ir rx
```

**Replay Signal**:
```
ir tx <file.ir>
```

**Example Output**:
```
IR:
Protocol: NEC
Address: 0x00, Command: 0x12
```

---

### BadUSB (Keyboard Emulation)

**Run Script**:
```
badusb run <script.txt>
```

**Example Script** (`payload.txt`):
```
DELAY 500
GUI r
DELAY 200
STRING cmd
ENTER
DELAY 300
STRING echo "Hello from KYNEE"
ENTER
```

**Warning**: BadUSB requires **explicit authorization** in RoE. Use only for approved targets.

---

## Python Integration

### Installation

```bash
pip install pyserial
```

### Example: RFID Scanner

```python
import serial
import time

class FlipperController:
    def __init__(self, port='/dev/ttyACM0', baudrate=115200):
        self.serial = serial.Serial(port, baudrate, timeout=1)
        time.sleep(2)  # Wait for Flipper boot
    
    def send_command(self, cmd):
        self.serial.write(f"{cmd}\r\n".encode())
        time.sleep(0.5)
        return self.serial.read(1024).decode()
    
    def rfid_read(self):
        return self.send_command('rfid read')
    
    def nfc_detect(self):
        return self.send_command('nfc detect')
    
    def close(self):
        self.serial.close()

# Usage
flipper = FlipperController()
result = flipper.rfid_read()
print(result)
flipper.close()
```

---

## KYNEĒ Agent Integration

### Collector Module

**Location**: `agent/aetherpi_agent/collectors/flipper.py`

**Features**:
- Auto-detect Flipper device (`/dev/ttyACM*`)
- Execute commands via CLI
- Parse output to JSON (per `schemas/findings.schema.json`)
- Enhanced audit logging (physical-layer actions)

**Engagement Flag**: Flipper actions require per-engagement opt-in (checkbox in console UI).

**Example Audit Log Entry**:
```json
{
  "timestamp": "2026-03-20T10:15:30Z",
  "engagement_id": "ENG-2026-051",
  "operator_id": "bob@pentestco.com",
  "action": "flipper_rfid_read",
  "device": "flipper_zero",
  "location": "Building A, Floor 2, Door 201",
  "justification": "Assess badge cloning risk per RoE Section 6.3",
  "outcome": "success",
  "findings": {
    "protocol": "HID ProxCard II",
    "facility_code": 123,
    "card_number": 45678
  }
}
```

---

## Security Considerations

### Authorization

- **Per-Engagement Opt-In**: Flipper actions must be explicitly enabled in console
- **RoE Requirement**: Physical testing must be documented in Rules of Engagement
- **Audit Trail**: Every Flipper command logged with operator ID, location, justification

### Ethical Boundaries

**Authorized**:
- Reading RFID badges (with consent)
- Testing access control systems (client-owned)
- IR remote cloning (non-destructive)
- Sub-GHz analysis (passive listening)

**Prohibited**:
- Cloning third-party badges without authorization
- Tampering with emergency systems (fire alarms, medical devices)
- Replaying signals that could cause harm (e.g., garage doors, vehicle fobs in traffic)
- BadUSB on personal devices (unless explicitly in scope)

---

## Troubleshooting

### Flipper Not Detected

```bash
lsusb  # Check for "Flipper Devices Inc."
ls -l /dev/ttyACM*  # Should show /dev/ttyACM0

# If missing, try:
sudo modprobe cdc_acm
```

### Permission Denied

```bash
sudo usermod -a -G dialout $USER
# Log out and back in

# Or (temporary):
sudo chmod 666 /dev/ttyACM0
```

### Flipper Hangs/Unresponsive

1. Disconnect USB
2. Reset Flipper: Hold BACK + LEFT for 10 seconds
3. Reconnect USB
4. Update firmware: [https://flipperzero.one/update](https://flipperzero.one/update)

### Commands Not Working

- Ensure Flipper firmware is up-to-date (v0.80.0+)
- Check for typos in CLI commands
- Try `help` to list available commands
- Consult [Flipper Docs](https://docs.flipperzero.one/)

---

## Future Enhancements

- **Bluetooth LE Control**: Wireless Flipper integration (eliminating USB cable)
- **Automated Workflows**: Scripted badge cloning + access control testing
- **Visual Dashboard**: Real-time Flipper status in console UI
- **Plugin System**: Custom Flipper Apps integration

---

## Resources

- **Official Docs**: [https://docs.flipperzero.one/](https://docs.flipperzero.one/)
- **Firmware**: [https://flipperzero.one/update](https://flipperzero.one/update)
- **CLI Reference**: [https://docs.flipperzero.one/development/cli](https://docs.flipperzero.one/development/cli)
- **Community**: [https://forum.flipperzero.one/](https://forum.flipperzero.one/)
- **Python Library**: [https://github.com/wh00hw/flipperzero-py](https://github.com/wh00hw/flipperzero-py)

---

**Last Updated**: February 24, 2026  
**Maintainer**: @zebadee2kk
