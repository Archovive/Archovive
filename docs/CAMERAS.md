# Cameras overview

Archovive presents the same analysis data in three deterministic perspectives.  
**Execution** requires `archovive_product_bundle_v4` (engine in [Archovive-core](https://github.com/Archovive/Archovive-core)).

| Camera | Lens | Audience | Primary artefacts |
|--------|------|----------|-------------------|
| **A — Operator** | Human decisions | Engineers, leads | `ARCHOVIVE_OUTPUT.md`, risk/compliance JSON |
| **B — Machine** | IR & anchors | CI, replay | `repro.json`, `drift_matrix.json`, `attestation.json` |
| **C — Evidence** | Audit & supply chain | Auditors, MCP, CI gates | `determinism.json`, `verify.json`, `sbom.json`, globals |

## Public repo (this repository)

| Camera | What you get here |
|--------|-------------------|
| A | `archovive camera operator --help`, `docs/OUTPUTS.md` |
| B | `archovive camera machine --help` (stub) |
| C | `archovive evidence --help`, `docs/SBOM.md`, `docs/DRIFT.md` |

## Product bundle

| Camera | CLI | MCP |
|--------|-----|-----|
| C | `archovive evidence`, `archovive camera evidence` | `archovive.evidence`, `archovive.global` |

Pilot benchmarks ship under `benchmarks/` inside the bundle ZIP (JSON only, no git clones).
