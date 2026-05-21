# Archovive CLI (Open Core)

Public surface for **Archovive v3** — policy packs, normative specs, fleet helper, and documentation.

The **analysis engine** (hypergraph, regulatory evaluation, Brain/Vault, attestation pipeline) is **not** in this repository. It ships as a separate licensed product bundle.

## What is included (MIT)

| Path | Purpose |
|------|---------|
| `bin/archovive` | CLI wrapper (delegates to licensed engine) |
| `archovive-fleet` | Multi-repo orchestration helper |
| `policy_packs/` | DORA / NIS2 / CRA / SOX JSON packs + `.sig` |
| `docs/` | Compiler spec, annotation schema, example output, positioning |
| `tools/render_dashboard.py` | Offline HTML dashboard from report JSON |
| `examples/sample_project/` | Minimal Git repo for trying the CLI |

## Quick start

```bash
# 1) Clone this repo
git clone https://github.com/archovive/archovive-cli.git
cd archovive-cli

# 2) Obtain the licensed engine bundle (private / commercial distribution)
#    Extract archovive_product_bundle_v3.tar.gz somewhere, then:
export ARCHOVIVE_ENGINE_ROOT=/path/to/archovive_product_bundle_v3

# 3) Install engine + validate open-core artifacts
./install_archovive.sh

# 4) Run analysis on the sample project
cd examples/sample_project
../../bin/archovive run
```

## Commands (via licensed engine)

- `archovive run` — full M1–M5 pipeline (tier-dependent)
- `archovive doctor` — environment check
- `archovive verify` — attestation verification
- `archovive sbom` / `archovive diff` / `archovive init --wizard`

See `docs/COMPILER_SPEC_V1.md` and `MANIFEST.json`.

## GitHub layout (`archovive` org)

| Repository | Visibility | Role |
|------------|------------|------|
| [**archovive-cli**](https://github.com/archovive/archovive-cli) | **Public** | This repo — policy packs, specs, CLI wrappers |
| [**archovive-core**](https://github.com/archovive/archovive-core) | **Private** | Deterministic engine (hypergraph, regulatory, attestation) |
| [**archovive**](https://github.com/archovive/archovive) | Public (legacy) | Historical product surface / CI badges |

Licensed customers receive the full product bundle tarball; `ARCHOVIVE_ENGINE_ROOT` points at that install or a private `archovive-core` checkout.

## License

- **This repo (`archovive-cli`):** MIT (`LICENSE`) — policy packs, specs, CLI wrappers, docs.
- **Engine (`archovive-core`):** Proprietary — private org repo, not in this tree.

## What is NOT in this repo (by design)

- `archovive_os/` engine source, hypergraph, regulatory engine, Brain/Vault
- `power_test/`, golden graph truth, enterprise slices
- Internal build pipelines

That IP remains in the private monorepo and licensed tarball only.
