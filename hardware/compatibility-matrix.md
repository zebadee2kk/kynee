# Hardware Compatibility Matrix

**Purpose**: Track tested hardware configurations to help users avoid compatibility issues.

---

## Testing Methodology

**Verification Criteria**:
- ✅ **Verified**: Tested by maintainers or trusted community members
- ⚠️ **Partial**: Works with caveats (driver issues, limited features)
- ❌ **Incompatible**: Does not work or requires significant workarounds
- ❓ **Untested**: Theoretically compatible, needs verification

**Test Procedures**:
1. Boot KYNEĒ agent on hardware
2. Run `iwconfig` (Wi-Fi), `hciconfig` (Bluetooth), `lsusb` (USB devices)
3. Execute test scans (`nmap`, `airodump-ng`, `hcitool scan`)
4. Verify JSON output validity against `schemas/findings.schema.json`
5. Check audit logs for completeness

---

## Compute Platforms

| Model | CPU | RAM | Status | Notes | Tester |
|-------|-----|-----|--------|-------|--------|
| Raspberry Pi 3 Model B+ | BCM2837B0 @ 1.4GHz | 1GB | ✅ Verified | Reference platform | @zebadee2kk |
| Raspberry Pi 4 Model B (2GB) | BCM2711 @ 1.5GHz | 2GB | ✅ Verified | Higher performance, more power | @zebadee2kk |
| Raspberry Pi 4 Model B (4GB) | BCM2711 @ 1.5GHz | 4GB | ✅ Verified | Best for AI workloads | Community |
| Raspberry Pi Zero 2 W | BCM2710A1 @ 1GHz | 512MB | ⚠️ Partial | Limited USB ports, slower | Community |
| Raspberry Pi 5 | BCM2712 @ 2.4GHz | 4GB | ❓ Untested | Expected to work | - |
| Orange Pi 5 | RK3588S @ 2.4GHz | 8GB | ❓ Untested | ARM64, Kali support unclear | - |
| ODROID-N2+ | S922X @ 2.2GHz | 4GB | ❓ Untested | Powerful, needs testing | - |

---

## Wi-Fi Adapters (Monitor Mode / Packet Injection)

| Model | Chipset | Bands | Monitor Mode | Injection | Driver | Status | Notes |
|-------|---------|-------|--------------|-----------|--------|--------|-------|
| **Alfa AWUS036ACH** | RTL8812AU | 2.4/5GHz | ✅ Yes | ✅ Yes | [aircrack-ng](https://github.com/aircrack-ng/rtl8812au) | ✅ Verified | **Recommended** |
| Alfa AWUS036NHA | AR9271 | 2.4GHz | ✅ Yes | ✅ Yes | Native (`ath9k_htc`) | ✅ Verified | Budget-friendly |
| TP-Link TL-WN722N **v1** | AR9271 | 2.4GHz | ✅ Yes | ✅ Yes | Native (`ath9k_htc`) | ✅ Verified | **v1 only** (v2/v3 incompatible) |
| TP-Link TL-WN722N v2/v3 | RTL8188EUS | 2.4GHz | ❌ No | ❌ No | N/A | ❌ Incompatible | Avoid |
| Panda PAU09 | RT5372 | 2.4/5GHz | ✅ Yes | ✅ Yes | Native (`rt2800usb`) | ✅ Verified | Good alternative |
| Alfa AWUS1900 | RTL8814AU | 2.4/5GHz | ✅ Yes | ✅ Yes | [aircrack-ng](https://github.com/aircrack-ng/rtl8814au) | ⚠️ Partial | High power, driver stability issues |
| Pi 3 built-in Wi-Fi | BCM43455 | 2.4/5GHz | ❌ No | ❌ No | N/A | ❌ Incompatible | Client mode only |

**Key Chipsets to Look For**:
- **Atheros AR9271**: Best native support, no driver install needed
- **Ralink RT5370/RT5372**: Native support, good for dual-band
- **Realtek RTL8812AU**: Powerful, but requires driver compilation

---

## Bluetooth Adapters

| Model | Chipset | Bluetooth Version | Status | Notes |
|-------|---------|-------------------|--------|-------|
| **Plugable USB-BT4LE** | BCM20702 | 4.0 LE | ✅ Verified | **Recommended** |
| ASUS USB-BT400 | BCM20702 | 4.0 LE | ✅ Verified | Good alternative |
| Kinivo BTD-400 | BCM20702 | 4.0 LE | ✅ Verified | Budget option |
| Pi 3 built-in Bluetooth | BCM43455 | 4.2 LE | ✅ Verified | Sufficient for basic tasks |
| TP-Link UB400 | CSR8510 | 4.0 | ⚠️ Partial | Occasional dropouts |
| Generic CSR 4.0 dongles | CSR8510 | 4.0 | ⚠️ Partial | Hit-or-miss quality |

---

## Flipper Zero

| Connection Method | Interface | Status | Notes |
|-------------------|-----------|--------|-------|
| **USB (Serial)** | `/dev/ttyACM0` | ✅ Verified | **Recommended** |
| UART (GPIO) | GPIO 14/15 | ✅ Verified | Requires custom cable |
| Bluetooth LE | BLE GATT | ❓ Untested | Potential future feature |

**Firmware Compatibility**:
- Official Firmware: v0.80.0+ — ✅ Verified
- Unleashed Firmware: v0.80.0+ — ✅ Verified
- RogueMaster Firmware: v0.80.0+ — ❓ Untested (should work)

---

## Power Solutions

| Model | Capacity | Output | Runtime (Pi 3) | Status | Notes |
|-------|----------|--------|----------------|--------|-------|
| **Anker PowerCore 20100** | 20,100 mAh | 5V/3A | 12-16 hours | ✅ Verified | **Recommended** |
| RAVPower 26800 | 26,800 mAh | 5V/3A | 18-22 hours | ✅ Verified | Extended missions |
| Xiaomi Mi 10000 | 10,000 mAh | 5V/2.4A | 6-8 hours | ✅ Verified | Compact, shorter runtime |
| Adafruit PowerBoost 1000C | N/A (LiPo) | 5V/2A | Varies | ⚠️ Partial | DIY, requires assembly |

**Under-Voltage Warnings**:
- Pi 3 requires **5V/2.5A minimum** under load
- Cheap power banks may cause `under-voltage detected` errors
- Use quality cables (20 AWG or lower) to minimize voltage drop

---

## MicroSD Cards

| Brand/Model | Capacity | Speed Class | Status | Notes |
|-------------|----------|-------------|--------|-------|
| **SanDisk Extreme** | 32GB | A1, UHS-I (100MB/s) | ✅ Verified | **Recommended** |
| Samsung EVO Plus | 64GB | A2, UHS-I (130MB/s) | ✅ Verified | Faster, larger |
| SanDisk High Endurance | 64GB | A1, UHS-I (100MB/s) | ✅ Verified | For heavy logging |
| Samsung PRO Endurance | 128GB | A1, UHS-I (100MB/s) | ✅ Verified | Long-term use |
| Generic Class 10 cards | Varies | Class 10 (10MB/s) | ⚠️ Partial | Slow, may cause lag |

**Recommendations**:
- **Minimum**: 32GB, Class 10 (A1 preferred)
- **Optimal**: 64GB, UHS-I, A2 (app performance)
- **High Endurance**: For write-heavy workloads (logging, packet captures)

---

## Enclosures

| Type | Model | Material | Cooling | Status | Notes |
|------|-------|----------|---------|--------|-------|
| Off-the-Shelf | Flirc Case | Aluminum | Passive (heatsink body) | ✅ Verified | **Recommended** for silent ops |
| Off-the-Shelf | Argon ONE | Plastic/Aluminum | Active (fan, 5V) | ✅ Verified | Better cooling, audible fan |
| Pelican Case | Pelican 1120 | Polymer | None | ✅ Verified | Rugged, waterproof |
| 3D-Printed | KYNEĒ v1 (custom) | PLA/ABS | Passive (vents) | ❓ Untested | Design in progress |

---

## Community Testing Queue

**Help us verify these configurations!**

| Hardware | Requested By | Tester Needed? |
|----------|--------------|----------------|
| Orange Pi 5 | Community | ✅ Yes |
| Raspberry Pi 5 | @zebadee2kk | ✅ Yes |
| Alfa AWUS1900 (long-term stability) | Community | ✅ Yes |
| TP-Link Archer T3U Plus (RTL8812BU) | Community | ✅ Yes |
| Flipper Zero via Bluetooth LE | @zebadee2kk | ✅ Yes |

**To Contribute**:
1. Test hardware per [Testing Methodology](#testing-methodology)
2. Document results (hardware specs, driver versions, test outcomes)
3. Open a PR updating this matrix
4. Include photos/screenshots if possible

---

## Troubleshooting

### Wi-Fi Adapter Not Detected
```bash
lsusb  # Check if USB device is visible
iwconfig  # Check if wireless interface appears

# If using RTL8812AU, install driver:
git clone https://github.com/aircrack-ng/rtl8812au.git
cd rtl8812au
make && sudo make install
sudo modprobe 88XXau
```

### Bluetooth Adapter Not Detected
```bash
hciconfig  # Check if Bluetooth controller is visible
sudo systemctl status bluetooth  # Ensure BlueZ is running

# Reset Bluetooth:
sudo hciconfig hci0 down
sudo hciconfig hci0 up
```

### Flipper Zero Not Connecting
```bash
ls -l /dev/ttyACM*  # Check if serial device exists
sudo chmod 666 /dev/ttyACM0  # Grant permissions

# Test connection:
screen /dev/ttyACM0 115200
# Press Enter, you should see Flipper CLI prompt
```

---

**Last Updated**: February 24, 2026  
**Maintainer**: @zebadee2kk  
**Contributors**: (to be listed as community members test hardware)
