# Bill of Materials (BOM)

## Core Hardware

### Compute Platform
- **Raspberry Pi 3 Model B+**
  - CPU: Broadcom BCM2837B0, Cortex-A53 (ARMv8) 64-bit @ 1.4GHz
  - RAM: 1GB LPDDR2
  - Storage: MicroSD card (32GB+ recommended, Class 10/UHS-I)
  - Ethernet: Gigabit (limited to ~300Mbps via USB 2.0)
  - Wi-Fi: 2.4GHz/5GHz 802.11ac (BCM43455), built-in
  - Bluetooth: 4.2 BLE, built-in
  - Price: ~£35-40

**Alternatives**:
- Raspberry Pi 4 Model B (2GB/4GB) — better performance, but higher power draw
- Raspberry Pi Zero 2 W — ultra-compact, but limited I/O

---

## Wireless Adapters

### Wi-Fi (Monitor Mode / Packet Injection)
- **Alfa AWUS036ACH** (recommended)
  - Chipset: Realtek RTL8812AU
  - Bands: 2.4GHz/5GHz dual-band
  - TX Power: 30dBm (1W)
  - Monitor mode: Yes
  - Packet injection: Yes (requires patched driver)
  - Kali Linux support: Excellent
  - Price: ~£45-50

**Alternatives**:
- Alfa AWUS036NHA (Atheros AR9271, 2.4GHz only, £30)
- TP-Link TL-WN722N v1 (Atheros AR9271, £15 — **verify v1, not v2/v3**)
- Panda PAU09 (Ralink RT5372, budget option, £20)

**Driver Notes**:
- RTL8812AU: Requires [aircrack-ng driver](https://github.com/aircrack-ng/rtl8812au)
- Atheros AR9271: Native support in Kali (`ath9k_htc` module)

### Bluetooth
- **Plugable USB-BT4LE** (recommended)
  - Chipset: Broadcom BCM20702
  - Bluetooth: 4.0 LE
  - Range: ~15m
  - Price: £12-15

**Alternatives**:
- ASUS USB-BT400 (Broadcom BCM20702, £15)
- Kinivo BTD-400 (Broadcom BCM20702, £10)
- Use built-in Bluetooth 4.2 (Pi 3 Model B+) for basic tasks

---

## Flipper Zero Integration

### Hardware
- **Flipper Zero**
  - Frequency: 433/868/915 MHz (sub-GHz), 13.56 MHz (NFC), 125 kHz (RFID LF)
  - GPIO: 18 pins (UART, I2C, SPI)
  - Price: ~£150-170
  - Availability: [flipperzero.one](https://flipperzero.one/) or authorized resellers

### Connectivity Options
1. **USB (recommended)**
   - Cable: USB-C to USB-A
   - Interface: Serial over USB (`/dev/ttyACM0` on Linux)
   - Library: [flipperzero-py](https://github.com/wh00hw/flipperzero-py)

2. **UART (advanced)**
   - Cable: Flipper GPIO breakout to Pi GPIO
   - Pinout: TX (Pin 13) → RX (Pi GPIO 15), RX (Pin 14) → TX (Pi GPIO 14)
   - Library: `pyserial`

**See**: [`hardware/flipper/integration-notes.md`](flipper/integration-notes.md) for wiring diagrams.

---

## Power

### Portable Power Bank (recommended)
- **Anker PowerCore 20100**
  - Capacity: 20,100 mAh
  - Output: 5V/3A (sufficient for Pi 3 + adapters)
  - Runtime: ~12-16 hours (depending on load)
  - Price: £30-35

**Alternatives**:
- RAVPower 26800mAh (longer runtime, £45)
- Xiaomi Mi Power Bank 10000mAh (compact, 6-8 hours, £20)

**Requirements**:
- Minimum output: 5V/2.5A (Pi 3 official spec)
- USB-A to USB-C or Micro-USB cable (depending on Pi model)

### LiPo Battery (advanced)
- **Adafruit PowerBoost 1000C** + 3.7V LiPo battery
  - Requires soldering/assembly
  - UPS-style setup (runs while charging)
  - Price: £25 (PowerBoost) + £15-30 (battery)

---

## Enclosure

### Off-the-Shelf Cases
- **Flirc Raspberry Pi 3 Case** (aluminum, passive cooling, £18)
- **SmartiPi Touch 2** (with touchscreen mount, £45)
- **Pelican 1120 Case** (waterproof, padded, £20)

### Custom 3D-Printed Enclosure
- Files: [`hardware/enclosure/kynee-case-v1.stl`](enclosure/) (to be added)
- Features:
  - Mounts for Pi 3, power bank, adapters
  - Ventilation holes
  - Antenna pass-throughs
  - VESA mount option
- Print time: ~8 hours (PLA, 0.2mm layer height)
- Material cost: ~£5

---

## Accessories

### Antennas (optional, for extended range)
- **2.4/5GHz Wi-Fi**: SMA 9dBi dual-band (£15)
- **Sub-GHz**: 433MHz 3dBi whip antenna for Flipper (£8)

### Cables
- USB-A to USB-C (for Flipper Zero): £5
- USB-A extension cables (30cm, for adapter placement): £3 each
- Micro-USB to USB-A (Pi 3 power): £3

### MicroSD Cards
- **SanDisk Extreme 32GB** (A1, UHS-I, 100MB/s read): £8
- **Samsung EVO Plus 64GB** (A2, UHS-I, 130MB/s read): £12

**Note**: Use "high endurance" cards for heavy logging workloads.

---

## Total Cost Estimate

### Minimal Configuration
| Item | Price (GBP) |
|------|-------------|
| Raspberry Pi 3 B+ | £38 |
| Alfa AWUS036ACH | £48 |
| Plugable USB-BT4LE | £13 |
| Anker PowerCore 20100 | £32 |
| SanDisk Extreme 32GB | £8 |
| Flirc Case | £18 |
| Cables & misc | £10 |
| **Total (no Flipper)** | **£167** |

### Full Configuration (with Flipper Zero)
| Item | Price (GBP) |
|------|-------------|
| Above minimal config | £167 |
| Flipper Zero | £160 |
| USB-C cable | £5 |
| **Total (with Flipper)** | **£332** |

---

## Compatibility Notes

### Tested Configurations
| Component | Status | Notes |
|-----------|--------|-------|
| Pi 3 B+ + Alfa AWUS036ACH | ✅ Verified | Requires driver install |
| Pi 3 B+ + TP-Link TL-WN722N v1 | ✅ Verified | Native support |
| Pi 4 + Alfa AWUS036ACH | ✅ Verified | Higher power draw |
| Pi Zero 2 W + Alfa AWUS036NHA | ✅ Verified | Limited USB ports |
| Flipper Zero via USB | ✅ Verified | Serial communication stable |

### Known Issues
| Component | Issue | Workaround |
|-----------|-------|------------|
| TP-Link TL-WN722N v2/v3 | No monitor mode | Use v1 only, or different adapter |
| Realtek RTL8812AU | Driver not in mainline | Install [aircrack-ng driver](https://github.com/aircrack-ng/rtl8812au) |
| Pi 3 USB power | Under-voltage warnings | Use 5V/3A power supply |

---

## Procurement Links

**UK Suppliers**:
- [The Pi Hut](https://thepihut.com/) (Pi, cases, accessories)
- [Pimoroni](https://shop.pimoroni.com/) (Pi, unique cases)
- [Amazon UK](https://amazon.co.uk/) (Wi-Fi adapters, power banks)

**Flipper Zero**:
- [Official Store](https://shop.flipperzero.one/) (direct, occasional stock issues)
- [Authorized Resellers](https://docs.flipperzero.one/basics/purchase) (Lab401, Hacker Warehouse)

---

**Last Updated**: February 24, 2026  
**Maintainer**: @zebadee2kk
