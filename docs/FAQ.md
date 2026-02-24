# Frequently Asked Questions (FAQ)

This FAQ covers legal, hardware, and usage questions about KYNEE.

---

## Legal and Ethics

**Q1: Is KYNEE legal to use?**
A: Yes, when you have written authorization from the system owner. Unauthorized use is illegal.

**Q2: Do I need a Rules of Engagement (RoE)?**
A: Yes. KYNEE requires a signed RoE that defines scope, time windows, and allowed methods.

**Q3: Can I use KYNEE on public Wi-Fi?**
A: Only if you have explicit written authorization from the network owner.

**Q4: What happens if I scan out of scope?**
A: Stop immediately, notify the client, and document the incident in the audit log.

**Q5: Does KYNEE allow social engineering?**
A: Only if the RoE explicitly authorizes it. Otherwise, it is prohibited.

---

## Hardware and OS

**Q6: What hardware is recommended?**
A: Raspberry Pi 3 Model B+ or better. See [hardware/bill-of-materials.md](../hardware/bill-of-materials.md).

**Q7: Does it work on Raspberry Pi 4 or Pi Zero 2 W?**
A: Yes, with varying performance. See [hardware/compatibility-matrix.md](../hardware/compatibility-matrix.md).

**Q8: Which Wi-Fi adapter should I buy?**
A: The Alfa AWUS036ACH is recommended for monitor mode and injection.

**Q9: Do I need a Bluetooth adapter?**
A: Not always. The Pi 3 built-in Bluetooth is enough for basic scans.

**Q10: What OS should I use?**
A: Kali Linux ARM (2024.1+).

---

## Installation and Setup

**Q11: Is there a packaged installer?**
A: Packaging is planned for Week 7. Until then, setup steps will evolve.

**Q12: Can I run the agent in a VM?**
A: It is possible for limited testing, but hardware-based scans require a Pi.

**Q13: Do I need Docker for the console?**
A: Docker is recommended for the fastest setup, but not required.

---

## Usage and Features

**Q14: Does KYNEE scan automatically?**
A: Only within the scope and schedule defined in the engagement.

**Q15: Can the AI assistant take actions on its own?**
A: No. Suggestions require explicit operator approval.

**Q16: Does KYNEE support wireless and Bluetooth testing?**
A: Planned for Week 3, with hardware-dependent support.

**Q17: Can I integrate Flipper Zero?**
A: Yes, for authorized physical-layer testing. See [docs/tutorials/flipper-integration.md](tutorials/flipper-integration.md).

**Q18: Does KYNEE store credentials?**
A: It should not store plaintext credentials. Secrets storage is planned for Week 8.

---

## Data Handling and Reporting

**Q19: Where are audit logs stored?**
A: On the agent and in the console, using append-only, hash-chained records.

**Q20: How long is data retained?**
A: Retention should match the RoE (typically 90 days).

**Q21: Can I export findings?**
A: Yes. The console will support Markdown and PDF exports (Week 5).

---

## Project Status

**Q22: Is KYNEE production-ready?**
A: Not yet. It is currently pre-alpha.

**Q23: How can I contribute?**
A: Start with [docs/getting-started.md](getting-started.md) and open a PR.

**Q24: Where do I report security vulnerabilities?**
A: Follow the instructions in [SECURITY.md](../SECURITY.md).