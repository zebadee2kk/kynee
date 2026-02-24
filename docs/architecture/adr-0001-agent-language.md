# ADR-0001: Agent Implementation Language

**Status**: Accepted  
**Date**: 2026-02-24  
**Deciders**: @zebadee2kk  
**Consulted**: Security community, Kali Linux maintainers  

---

## Context

The KYNEĒ agent runs on Raspberry Pi 3 (1GB RAM, ARM architecture) and must:

- Integrate with existing security tools (nmap, airodump-ng, hcitool)
- Parse command-line tool outputs and produce structured JSON
- Communicate securely with the console (WireGuard, HTTPS)
- Run as a systemd service with minimal resource usage
- Support rapid development and testing

**Language options considered**:

1. **Python**
   - ✅ Native support in Kali Linux
   - ✅ Rich ecosystem (pyserial, requests, schedule)
   - ✅ Easy subprocess handling and text parsing
   - ✅ Fast prototyping
   - ⚠️ Higher memory usage (~50-100MB baseline)
   - ⚠️ GIL limits concurrency (mitigated by asyncio)

2. **Go**
   - ✅ Compiled binaries (single file deployment)
   - ✅ Low memory usage (~10-20MB)
   - ✅ Native concurrency (goroutines)
   - ⚠️ Cross-compilation for ARM required
   - ⚠️ Steeper learning curve for contributors
   - ⚠️ Less mature security tool libraries

3. **Rust**
   - ✅ Memory safety guarantees
   - ✅ Excellent performance
   - ⚠️ Longer development time
   - ⚠️ Smaller contributor pool
   - ⚠️ Compilation times on Pi 3 (cross-compile required)

4. **Bash**
   - ✅ Ubiquitous in Kali Linux
   - ✅ Direct tool invocation
   - ⚠️ Error handling is fragile
   - ⚠️ No structured data handling
   - ⚠️ Hard to test and maintain

---

## Decision

**We will implement the agent in Python 3.11+.**

### Rationale

1. **Ecosystem Fit**
   - Kali Linux ships with Python 3 and extensive libraries
   - Most security tools output text; Python's string handling is superior
   - Libraries like `pyserial` (Flipper), `pywireguard`, `schedule` are mature

2. **Development Speed**
   - 8-week roadmap requires rapid iteration
   - Python allows quick prototyping and testing
   - Large contributor pool familiar with Python

3. **Resource Usage Acceptable**
   - Pi 3 has 1GB RAM; 50-100MB for Python is acceptable
   - Agent is I/O-bound (waiting on nmap, etc.), not CPU-bound
   - asyncio mitigates GIL limitations for concurrent network operations

4. **Integration**
   - Subprocess handling (`subprocess.run`) is reliable
   - JSON schema validation via `jsonschema` library
   - WireGuard via `subprocess` or `pywireguard` bindings

### Performance Mitigation

- Use `asyncio` for non-blocking I/O
- Profile with `cProfile` and optimize hot paths
- Consider Cython for critical sections if needed (future)

---

## Consequences

### Positive

- ✅ Fast development (aligns with 8-week roadmap)
- ✅ Easy onboarding for contributors
- ✅ Rich testing ecosystem (pytest, unittest)
- ✅ Native Kali Linux integration

### Negative

- ⚠️ Higher memory usage than Go/Rust (mitigated: Pi 3 has sufficient RAM)
- ⚠️ Requires Python runtime on target (mitigated: Kali ships with Python)
- ⚠️ Slower startup than compiled languages (mitigated: runs as long-lived service)

### Neutral

- Packaging as `.deb` with Python dependencies (standard for Kali)
- Future migration to Go possible if performance becomes critical (data model defined via JSON schemas allows language-agnostic rewrite)

---

## Related Decisions

- [ADR-0003: Data Serialization Format](adr-0003-data-serialization.md) (JSON schemas allow language independence)

---

**Last Updated**: February 24, 2026  
**Maintained By**: @zebadee2kk
