# Installation — Archovive product bundle v4

Technical install and run reference for pilots. Detail: `docs/` (pipeline, artefacts, MCP, troubleshooting).

## Footprint

| Stage | Disk |
|-------|------|
| Zip download | ~0.5–0.7 MB (`archovive_product_bundle_v4.zip`, product + optional `benchmarks/`) |
| Extracted | ~10 MB (product); +benchmark JSONs if present |
| After `./install_archovive.sh` | **~500–700 MB** (local `.venv`) |

Pilot archives use the **same** zip name and top-level folder as this document: `archovive_product_bundle_v4.zip` → `archovive_product_bundle_v4/`.

## Requirements

| Requirement | Detail |
|-------------|--------|
| OS | Linux, macOS, or WSL2 |
| Python | **3.11+** |
| Git | Recommended for analysis root detection |
| Disk | ~700 MB free for venv |

## Install

```bash
unzip archovive_product_bundle_v4.zip
cd archovive_product_bundle_v4
./install_archovive.sh
```

| Flag | Effect |
|------|--------|
| `--minimal-venv` | Smaller venv; **no MCP** / trust extras |
| `--global-link` | Symlink `archovive` to `~/.local/bin` or `/usr/local/bin` |

## License tier

Default: **`ci`** in `archovive_license.json` at **bundle root**.

| Tier | Enable |
|------|--------|
| **gov** (full artefacts) | `cp licenses/archovive_license_gov.json archovive_license.json` |
| One-shot | `export ARCHOVIVE_LICENSE_TIER=gov` |

Artefact list: `docs/OUTPUTS.md`.

## CLI

Run from your project directory (not from **bundle root**):

```bash
cd /path/to/your/git-project
/path/to/archovive_product_bundle_v4/bin/archovive run
echo exit=$?
```

| Exit | Meaning |
|------|---------|
| 0 | Pass |
| 1 | Drift |
| 2 | Policy / regulatory |
| 3 | Engine error |
| 4 | Misuse (e.g. run inside bundle root) |

Further commands: `init`, `verify`, `doctor`, `diff`, `sbom` — see `MANIFEST.json` → `cli_commands`.

## CI

Templates in `ci/`:

| Platform | File |
|----------|------|
| GitHub Actions | `ci/archovive-run.yml` |
| GitLab | `ci/archovive-gitlab-ci.yml` |
| Jenkins | `ci/archovive-jenkins.groovy` |
| Azure Pipelines | `ci/archovive-azure-pipelines.yml` |

```bash
CI=true /path/to/archovive_product_bundle_v4/bin/archovive run
```

## MCP (MCP-compatible client)

1. Full install (not `--minimal-venv`).
2. Stdio server setup: `docs/MCP_QUICKSTART.md`.
3. Tool API: `docs/MCP_PROMPT.md`.

`.cursor/mcp.json` is a **format example only**. Set `command` to `.venv/bin/python3` and `ARCHOVIVE_REPO` to the absolute **bundle root**.

## Environment variables

See `docs/ENVIRONMENT_VARIABLES.md`.

Minimal exports:

```bash
export ARCHOVIVE_REPO="/absolute/path/to/archovive_product_bundle_v4"
export ARCHOVIVE_COMPILE=runtime
```

## Developer documentation

| Doc | Topic |
|-----|--------|
| `docs/ARCHITECTURE.md` | Package layout |
| `docs/PIPELINE.md` | M1–M5 phases |
| `docs/OUTPUTS.md` | Output artefacts |
| `docs/TROUBLESHOOTING.md` | Common fixes |
| `docs/MCP_QUICKSTART.md` | MCP setup |
| `docs/MCP_PROMPT.md` | Tool parameters |

## Validation record

`test_nachweise/` — tier runs, visible output previews, release lock.
