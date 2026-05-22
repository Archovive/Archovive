# Archovive — Deterministic Architecture Governance (Open Core)

Public **CLI surface**, **policy packs**, **normative specs**, and **documentation**.

The deterministic **engine**, Evidence Camera runtime, SBOM pipeline, verify chain, and **`archovive_product_bundle_v4.zip`** are built from **[Archovive-core](https://github.com/Archovive/Archovive-core)** (private). This repository is **MIT open-core** — not the engine.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Quick start (pilot)

```bash
git clone https://github.com/Archovive/Archovive.git
cd archovive
# Place archovive_product_bundle_v4.zip in this directory
./install_archovive.sh
source ./archovive.env
archovive --help
archovive run /path/to/your-repo
```

| Mode | When |
|------|------|
| **After `./install_archovive.sh`** | `ARCHOVIVE_ENGINE_ROOT` → `archovive_product_bundle_v4/`; full engine |
| **Without ZIP** | `archovive --help` / `doctor` only; `run` points to the bundle |

See `docs/INSTALL.md`.

---

## What this repository contains (MIT)

| Path | Purpose |
|------|---------|
| `archovive/cli/` | v4 CLI router (help + stubs) |
| `bin/archovive` | Shell wrapper → bundle or public router |
| `policy_packs/` | DORA / NIS2 / CRA / SOX JSON + signatures |
| `docs/` | INSTALL, OUTPUTS, CAMERAS, MCP, SBOM, DRIFT, compiler spec |
| `archovive-fleet` | Multi-repo helper |
| `tools/render_dashboard.py` | Offline HTML from report JSON |
| `examples/sample_project/` | Minimal sample repo |

## What is **not** here

Engine, IR compiler, gov slice, vault, evidence implementation, benchmarks, bundle build scripts → **Archovive-core**.

---

## Product bundle (pilot)

```text
archovive_product_bundle_v4.zip  →  archovive_product_bundle_v4/
```

See [docs/INSTALL.md](docs/INSTALL.md). Optional `benchmarks/` JSON evidence inside the ZIP.

---

## Documentation

| Doc | Topic |
|-----|--------|
| [docs/INSTALL.md](docs/INSTALL.md) | Bundle install |
| [docs/OUTPUTS.md](docs/OUTPUTS.md) | Artefacts & license tiers |
| [docs/CAMERAS.md](docs/CAMERAS.md) | Operator / Machine / Evidence |
| [docs/MCP.md](docs/MCP.md) | MCP (in bundle) |
| [docs/SBOM.md](docs/SBOM.md) | `file_hashes` |
| [docs/DRIFT.md](docs/DRIFT.md) | `unmeasured` / `null` |
| [docs/COMPILER_SPEC_V1.md](docs/COMPILER_SPEC_V1.md) | Normative spec |

---

## Open-core model

```text
Archovive (public)        →  CLI + policy packs + docs
Archovive-core (private)  →  Engine + OS + product bundle + benchmarks
```

[SECURITY.md](SECURITY.md)
