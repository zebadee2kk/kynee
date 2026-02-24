# ADR-0001: Agent Implementation Language

## Status
**Accepted** (2026-02-24)

## Context

The KYNEĒ agent runs on resource-constrained Raspberry Pi 3 hardware (1GB RAM, ARM CPU) and must:

- Interface with Linux security tools (nmap, airodump-ng, hcitool)
- Parse command-line tool output and convert to JSON
- Communicate securely with a remote console
- Maintain audit logs with cryptographic integrity
- Run as a systemd service with minimal overhead

**Options Considered**:

1. **Python 3.11+**
   - Pros: Rich ecosystem (subprocess, asyncio, cryptography), rapid development, Kali Linux pre-installed
   - Cons: Higher memory usage (~50MB base), slower than compiled languages

2. **Go**
   - Pros: Single binary, low memory (~10MB), fast, good concurrency
   - Cons: Verbose for CLI tool wrappers, smaller security tool ecosystem

3. **Rust**
   - Pros: Memory-safe, zero-cost abstractions, excellent performance
   - Cons: Steep learning curve, longer compile times, cross-compilation complexity for ARM

4. **Shell Scripts (Bash)**
   - Pros: Universal, minimal dependencies
   - Cons: Poor error handling, hard to maintain, no strong typing

## Decision

**Python 3.11+** for the agent implementation.

### Rationale

1. **Ecosystem**: Python has mature libraries for:
   - CLI tool wrappers (`subprocess`, `sh`)
   - JSON/YAML parsing (`json`, `pyyaml`)
   - Cryptography (`cryptography`, `pyca`)
   - Networking (`asyncio`, `aiohttp`)
   - Serial communication (`pyserial` for Flipper Zero)

2. **Kali Linux Native**: Python 3.11+ is pre-installed on Kali ARM, reducing image size.

3. **Rapid Prototyping**: Week 1-8 roadmap requires fast iteration; Python enables this.

4. **Community**: Security tools often have Python APIs or wrappers (e.g., `python-nmap`).

5. **Performance Sufficient**: Agent performs mostly I/O-bound tasks (network scans, file writes); CPU is not bottleneck.

### Mitigations for Cons

- **Memory**: Use lightweight libraries, avoid heavy frameworks (e.g., Django).
- **Speed**: Profile hot paths, offload heavy computation to C extensions if needed.
- **Typing**: Use `mypy` for static type checking, enforce via CI.

## Consequences

### Positive

- Fast development velocity (critical for 8-week roadmap)
- Strong integration with Kali Linux ecosystem
- Easier onboarding for contributors (Python is widely known)
- Rich testing ecosystem (`pytest`, `unittest`)

### Negative

- Higher memory footprint vs. Go/Rust (~50MB vs. ~10MB)
- Requires venv or packaging for dependency isolation
- Slower execution vs. compiled languages (acceptable for I/O-bound workloads)

### Neutral

- May consider Go/Rust rewrite for specific modules (e.g., high-throughput packet processing) in future versions.

## Alternatives Revisited

If performance becomes an issue post-v1.0:

- Profile with `cProfile`, optimize hot paths.
- Use `Cython` or `PyPy` for JIT compilation.
- Hybrid approach: Python orchestration + Go/Rust microservices for compute-heavy tasks.

---

**Decision Maker**: @zebadee2kk  
**Date**: February 24, 2026  
**Supersedes**: None
