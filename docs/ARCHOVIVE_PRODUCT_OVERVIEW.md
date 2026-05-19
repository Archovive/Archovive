# Archovive — Full Overview

> **GitHub landing:** see [../README.md](../README.md) for the short entry point.

**Deterministic Architecture Governance.**  
One command, one verdict, one immutable proof.

Archovive is not a scanner. It is a sovereign operating system for software architecture compliance.

It takes any repository or audit signal, compiles it into a unified hypergraph, evaluates it against regulatory policies (DORA, NIS2, BAIT, EU Cyber Resilience Act), and returns a single, cryptographically sealed verdict — **PASS** or **BLOCK** — with enumerated reasons, economic impact, and a forensically replayable proof.

---

## Why Archovive exists

In 2025, the European Union began enforcing DORA, NIS2, and the Cyber Resilience Act. For the first time, **software architecture itself became a regulated asset**. Enterprises must now prove — not document, but **mathematically prove** — that their systems comply with structural, economic, and safety requirements.

No existing tool does this.

- SAST, SCA, GRC platforms, and architecture scanners produce **signals**.
- None of them produce **decisions**.
- None of them produce **court-admissible evidence**.

Archovive was built to fill that gap. It is the first deterministic pipeline that transforms external signals and internal code into a single, non-repudiable architecture verdict, backed by a Merkle-rooted proof bundle and zero-knowledge attestation (ZKAP-ready).

---

## What Archovive does

### One command

```bash
archovive analyze <target> --out attest.json
```

`<target>` can be a local repository, a `synthetic://` URI, or a raw audit signal (JSON file).

### One verdict

Every run produces a **RunVerdict**:

| Verdict | Meaning |
|---------|---------|
| **PASS** | No regulatory or structural violation detected |
| **BLOCK** | Specific rule violated, with `block_reason`, `business_impact_eur`, and `control_verdict_hash` |

In attestation artifacts, regulatory packs surface `COMPLIANT` / `NON_COMPLIANT`; **BLOCK** is the enforcement semantics when governance rules fail.

### One immutable proof

The run is sealed into a **ProofBundle** — replayable, verifiable, and auditable (ZKAP-ready).

---

## The three-step journey

1. **`archovive bootstrap`** — self-attestation (`BOOTSTRAP: PASS`)
2. **`archovive simulate`** — guided DORA violation walkthrough
3. **`archovive analyze`** — sovereign kit + optional PDF export

---

## Quick start

```bash
pip install archovive-core          # private registry (required)
pip install archovive
archovive bootstrap
archovive simulate
archovive analyze . --out attest.json --package-dir ./sovereign-kit
archovive-attestation export ./sovereign-kit/attest.json --pdf
```

---

## Documentation

| Document | Content |
|----------|---------|
| [ARCHOVIVE_SOVEREIGN_SPEC_V1.md](ARCHOVIVE_SOVEREIGN_SPEC_V1.md) | Product specification |
| [ARCHOVIVE_BINARY_SUITE.md](ARCHOVIVE_BINARY_SUITE.md) | Multi-binary suite |
| [ARCHOVIVE_OPEN_CORE_MODEL.md](ARCHOVIVE_OPEN_CORE_MODEL.md) | Open-core distribution |
| [RELEASE_NOTES_v1.0.0.md](RELEASE_NOTES_v1.0.0.md) | Release checklist |

---

## License

Public components: **MIT** ([LICENSE](../LICENSE)).  
**archovive-core**: commercial — core@archovive.com
