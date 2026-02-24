# ADR-0001: Agent Implementation Language

**Status**: Proposed  
**Date**: 2026-02-24  
**Deciders**: @zebadee2kk, Architecture Team  
**Technical Story**: Week 1 roadmap milestone

---

## Context

The KYNEĒ agent runs on Raspberry Pi 3 (ARM, 1GB RAM) and must:

- Execute security tools (nmap, airodump-ng, hcitool)
- Parse tool output and generate structured JSON
- Communicate securely with the console (WireGuard, HTTPS)
- Enforce policy constraints (scope, rate limits)
- Log all actions immutably
- Run as a systemd service (daemon)
- Be maintainable by security professionals (not just developers)

We need to choose a primary implementation language.

---

## Decision

**Use Python 3.11+ as the primary agent language.**

### Rationale

1. **Ecosystem**: Rich libraries for security tooling (`scapy`, `pyserial`, `requests`, `cryptography`)
2. **Kali Integration**: Python is pre-installed on Kali Linux, first-class support
3. **Parsing**: Easy to parse tool output (regex, subprocess, json)
4. **Rapid Development**: Faster prototyping, good for 8-week timeline
5. **Community**: Large pool of security professionals know Python
6. **ARM Performance**: Acceptable for I/O-bound tasks (scanning, network comms)

---

## Consequences

### Positive

- Faster development (mature libraries, less boilerplate)
- Easier to onboard contributors (pentesters familiar with Python)
- Good integration with Kali tools (most have Python bindings)
- `asyncio` for concurrent scanning

### Negative

- Slower than compiled languages (Go, Rust) for CPU-intensive tasks
- Higher memory footprint (~30-50MB baseline)
- GIL limits true parallelism (mitigated by subprocess/multiprocessing)
- Packaging overhead (virtualenv, dependencies)

### Neutral

- Will use `subprocess` to call external tools (nmap, airodump)
- Performance-critical parsers can be written in Cython if needed

---

## Alternatives Considered

### Alternative 1: Go

**Pros**:
- Compiled, fast, small binary
- Excellent concurrency (goroutines)
- Cross-compilation for ARM trivial
- Low memory footprint

**Cons**:
- Smaller security tooling ecosystem
- Steeper learning curve for non-Go developers
- Less mature Kali integration
- Longer development time

**Why Rejected**: Development speed and ecosystem trade-offs not worth performance gains for I/O-bound workload.

### Alternative 2: Rust

**Pros**:
- Memory safety without GC
- Excellent performance
- Modern tooling (cargo)

**Cons**:
- Steep learning curve
- Smaller security community
- Longer compilation times
- Overkill for subprocess orchestration

**Why Rejected**: Too slow to prototype for 8-week timeline, limited security tool bindings.

### Alternative 3: Bash Scripts

**Pros**:
- Native to Linux
- Direct tool invocation
- Minimal dependencies

**Cons**:
- Error handling nightmare
- Complex JSON parsing
- No type safety
- Hard to test
- Not scalable for policy engine, audit logging

**Why Rejected**: Unmaintainable for anything beyond trivial scripts.

---

## Implementation Notes

- Use `pyproject.toml` (PEP 518) for packaging
- Target Python 3.11+ (pattern matching, better asyncio)
- Use `ruff` for linting (faster than flake8/pylint)
- Use `black` for formatting (consistent style)
- Use `pytest` for testing
- Package as wheel + Debian `.deb` for easy installation

---

## References

- [Python on Kali](https://www.kali.org/docs/general-use/python-tutorials/)
- [Raspberry Pi Python Performance](https://www.raspberrypi.com/news/python-comes-to-the-raspberry-pi/)
- [Subprocess Security](https://docs.python.org/3/library/subprocess.html#security-considerations)

---

**Last Updated**: February 24, 2026  
**Status**: Proposed (requires maintainer approval)
