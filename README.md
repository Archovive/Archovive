# Archovive

**Deterministic Architecture Governance.**  
**One command. One verdict. One immutable proof.**

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![archovive-public-ci](https://github.com/Archovive/Archovive/actions/workflows/archovive-public-ci.yml/badge.svg)](https://github.com/Archovive/Archovive/actions/workflows/archovive-public-ci.yml)
[![PDF Gate](https://img.shields.io/badge/PDF%20Gate-archovive--public--ci-0A9396)](https://github.com/Archovive/Archovive/actions/workflows/archovive-public-ci.yml#pdf-gate)
[![Open Core](https://img.shields.io/badge/model-open--core-purple.svg)](docs/ARCHOVIVE_OPEN_CORE_MODEL.md)
[![Security](https://img.shields.io/badge/security-policy-blue.svg)](SECURITY.md)

Archovive is a **sovereign operating system for software architecture compliance**.  
It compiles any repository or audit signal into a unified hypergraph, evaluates it against regulatory policies (**DORA**, **NIS2**, **BAIT**, **CRA**), and produces a single, cryptographically sealed verdict — with a **replayable proof bundle**.

| | |
|---|---|
| **Releases** | [v1.0.0](docs/RELEASE_NOTES_v1.0.0.md) · [GitHub Releases](https://github.com/Archovive/Archovive/releases) |
| **Overview** | [docs/ARCHOVIVE_PRODUCT_OVERVIEW.md](docs/ARCHOVIVE_PRODUCT_OVERVIEW.md) |
| **Demo** | `archovive-cli simulate` |
| **Core access** | core@archovive.com |
| **Security** | [SECURITY.md](SECURITY.md) |

---

## Terminal walkthrough (60 seconds)

```text
$ archovive bootstrap
=== [ARCHOVIVE v1] Sovereign Bootstrap ===
[1/5] SPEC v4 Hash .................. OK
[2/5] Health Certificate v2 ......... OK
[3/5] Epoch Binding ................. OK
[4/5] Hypervisor Binding ............ OK
[5/5] Identity Hash Stability ....... OK
BOOTSTRAP: PASS

$ archovive simulate
=== [ARCHOVIVE v1] Truth Simulator ===
[1/5] INGESTION (L1)     H_verdict: 7f3a9c2b…
[2/5] RUNTIME (L2)       hypervisor_binding: a91e…
[3/5] GOVERNANCE (L3)    Verdict: NON_COMPLIANT
[4/5] ATTESTATION        attestation_hash: c4e8…
[5/5] REPLAY             BIT-IDENTICAL
SIMULATE: PASS
```

---

## Installation (with Core registry)

`archovive` requires the commercial engine **`archovive-core`** from a private package index.

```bash
# 1. Engine (licensed — request access at core@archovive.com)
export ARCHOVIVE_CORE_INDEX_URL="https://pypi.archovive.com/simple/"
pip install archovive-core --extra-index-url "${ARCHOVIVE_CORE_INDEX_URL}"

# 2. Public product CLI (PyPI or git)
pip install archovive
```

GitHub Actions: set repository secret `ARCHOVIVE_CORE_INDEX_URL` to the same index URL.

## Quick start

```bash
archovive-cli bootstrap
archovive-cli simulate
archovive-cli analyze /path/to/repo --out attest.json --package-dir ./sovereign-kit
archovive-attestation export ./sovereign-kit/attest.json --pdf
```

Prerequisites: Python ≥ 3.12 · PDF export: `pandoc` + `pdflatex` (validated in CI **pdf-gate**)

See [SECURITY.md](SECURITY.md) for disclosure policy and supported versions.

---

## The sovereign journey

| Step | Command | What you get |
|------|---------|----------------|
| **Bootstrap** | `archovive bootstrap` | System attests to itself |
| **Simulate** | `archovive simulate` | Guided DORA violation walkthrough |
| **Analyze** | `archovive analyze <target> --out attest.json` | Sovereign attestation package |
| **Export** | `archovive-attestation export attest.json --pdf` | Auditor-ready PDF |

---

## Sovereign Kit output

```text
sovereign-kit/
├── BUNDLE_MANIFEST.json
├── attest.json
├── attest.md
├── attest.pdf
├── health_certificate_v2.json
├── spec_v4.json
├── ledger.jsonl
└── zkap_attestation.json
```

Never commit generated kits — see [.gitignore](.gitignore).

---

## Supported regulations

| Pack | Focus |
|------|--------|
| **DORA** | ICT risk, testing, ICS criticality |
| **NIS2** | Supply chain, governance |
| **BAIT** | Operational resilience |
| **SOX** | ITGC mapping |
| **EU CRA** | Software-product compliance |

---

## Open-core model

| Repository | License | Contents |
|------------|---------|----------|
| **archovive** (this repo) | MIT | CLI, product surface, five product docs |
| **archovive-core** (private) | Commercial | Engine, hypergraph, policies, proof pipeline |

Request engine access: **core@archovive.com**

---

## Documentation

- [Product overview](docs/ARCHOVIVE_PRODUCT_OVERVIEW.md)
- [Sovereign spec v1](docs/ARCHOVIVE_SOVEREIGN_SPEC_V1.md)
- [Binary suite](docs/ARCHOVIVE_BINARY_SUITE.md)
- [Open-core model](docs/ARCHOVIVE_OPEN_CORE_MODEL.md)
- [Release notes v1.0.0](docs/RELEASE_NOTES_v1.0.0.md)

---

## The first sovereign verdict

> *Archovive doesn't ask for trust. It proves its own — and then it proves yours.*

```bash
archovive-cli bootstrap
```

If it passes, the system is sovereign — and ready to attest anything else.
