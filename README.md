# Archovive — Deterministic Architecture Governance (Open Core)

Public **installer**, **tier profiles**, **normative docs**, and **product manifest** for v5.

The deterministic **engine**, frozen **binary**, and **`archovive-enterprise-5.0.0.zip`** are built from **[Archovive-core](https://github.com/Archovive/Archovive-core)** (private). This repository is **MIT open-core** — not the engine.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Quick start (v5.0.0)

```bash
git clone https://github.com/Archovive/Archovive.git
cd Archovive
# Download from GitHub Release v5.0.0:
#   archovive-enterprise-5.0.0.zip + .sha256 + archovive.slsa.provenance.json
./install_archovive.sh
source ./archovive.env
archovive --version
archovive doctor
archovive ask "why blocked?"
```

Release notes: [docs/RELEASE_NOTES_v5.0.0.md](docs/RELEASE_NOTES_v5.0.0.md)

| Mode | When |
|------|------|
| **After `./install_archovive.sh`** | `PATH` includes `archovive-enterprise-5.0.0/bin`; full v5 binary |
| **Without ZIP** | Clone only — download release assets beside `install_archovive.sh` first |

See `docs/README.md` (customer POV).

---

## What this repository contains (MIT)

| Path | Purpose |
|------|---------|
| `install_archovive.sh` | v5 bundle unpack + env wiring |
| `MANIFEST.json` / `RELEASE.lock.json` | Product package pin (version, binary SHA) |
| `docs/` | Customer docs (README, LEXIKON, ENTERPRISE, tutorials) |
| `deploy/profiles/` | personal / team / enterprise tier profiles |
| `policy_packs/` | DORA / NIS2 / CRA / SOX JSON + signatures |
| `examples/` | Sample repos |

## What is **not** here

Engine source, runtime monorepo, benchmarks, bundle build scripts → **Archovive-core**.

---

## Product bundle (v5 stable)

```text
archovive-enterprise-5.0.0.zip  →  archovive-enterprise-5.0.0/
  bin/         archovive, archovive-mcp (XDG-aware wrappers)
  libexec/     PyInstaller runtime (read-only)
  share/       docs, legal, examples, templates
  scripts/     install.sh, verify_signature.sh, setup_license.sh
  metadata/    build_manifest.json, sha256.txt, provenance
```

Truth surfaces (must match): `ask` = `chat` = `governance decide`

---

## Open-core model

```text
Archovive (public)        →  installer + docs + tier profiles
Archovive-core (private)  →  engine + kernel + binary build + releases
```

[SECURITY.md](SECURITY.md)
