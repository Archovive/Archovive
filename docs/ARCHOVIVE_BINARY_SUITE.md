# Archovive v1 — Multi-Binary Kit

Seven sovereign console scripts share one engine (`archovive_os`). Each binary is a **2–5 line wrapper** with distinct branding — no duplicated pipe logic.

## Binaries

| Binary | Role | Example |
|--------|------|---------|
| `archovive-cli` | Full product surface | `archovive-cli bootstrap` |
| `archovive` | Alias → `archovive-cli` | `archovive simulate` |
| `archovive-core` | L1 hermetic truth | `archovive-core ingest repo in.json out.json` |
| `archovive-runtime` | L2 operational truth | `archovive-runtime analyze input.json --out out.json` |
| `archovive-audit` | L3 governance | `archovive-audit replay pipe_l3_dora_violation` |
| `archovive-health` | Health Certificate v2 | `archovive-health verify ./kit/health_certificate_v2.json` |
| `archovive-spec` | SPEC v4 utility | `archovive-spec hash ./kit/spec_v4.json` |
| `archovive-attestation` | Export pipeline | `archovive-attestation export attest.json --pdf` |

## Install (Repo A — public)

```bash
pip install archovive-core   # private registry
pip install archovive
```

Repo A ships **`archovive`**, **`archovive-cli`**, and **`archovive-attestation`**.  
Core binaries (`archovive-core`, `archovive-runtime`, `archovive-audit`, …) ship with **archovive-core** (private).

## Verify locally (monorepo / licensed install)

```bash
archovive bootstrap
archovive simulate
```

## Release (platform binaries)

Console scripts are native on each platform after `pip install`. For **standalone** executables (air-gap USB, no Python on target):

1. Install PyInstaller in a release venv: `pip install pyinstaller`
2. For each entry point in `archovive_os/cli/entrypoints.py`, build:

```bash
pyinstaller --onefile --name archovive-cli \
  --copy-metadata archovive_os \
  -c 'from archovive_os.cli.entrypoints import main_cli; main_cli()'
```

Repeat for `archovive-core`, `archovive-runtime`, etc. Ship all seven binaries plus `BUNDLE_MANIFEST.json` from a reference sovereign kit.

**Dual-repo note:** public Repo A may ship wrappers + docs only; private Repo B ships engine wheel consumed as dependency.

## Implementation

| File | Purpose |
|------|---------|
| `cli/entrypoints.py` | setuptools `project.scripts` targets |
| `cli/binary_kit.py` | Branding + version metadata |
| `cli/binary_dispatch.py` | Per-mode argparse + dispatch |
| `cli/main.py` | Full CLI parser (`_build_parser`, `_dispatch_full`) |
