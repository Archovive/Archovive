# Archovive v1 — Sovereign Architecture Truth System

> **Landing:** [../README.md](../README.md) · **Overview:** [ARCHOVIVE_PRODUCT_OVERVIEW.md](ARCHOVIVE_PRODUCT_OVERVIEW.md) · **Release:** [RELEASE_NOTES_v1.0.0.md](RELEASE_NOTES_v1.0.0.md)

Archovive v1 is the **product surface** on top of the frozen Pipe v4.0 engine. One command, one proof, one bundle.

## Product promise

> Gib mir ein System — ich gebe dir die Wahrheit.

## 1. Product surface

### 1.1 Entry point (CLI v1)

```bash
archovive analyze <target> --out attest.json
```

Optional full Sovereign Kit:

```bash
archovive analyze <target> --out attest.json --package-dir ./sovereign-kit
```

| Step | Engine | Layer |
|------|--------|-------|
| Hermetic truth | `run_pipe` | L1 (via L3) |
| Runtime truth | `run_runtime_pipe` | L2 (via L3) |
| Governance truth | `run_audit_pipe` | L3 |
| Attestation | `product_v1.analyze` | v1 bundle |

`<target>` may be:

- Repository path (uses `audit_input.json` if present, else built-in DORA demo input)
- `synthetic://…` URI
- Path to a `.json` audit input file

On a TTY, bootstrap runs first (integrity + SPEC + Health Certificate gate).

### 1.2 Sovereign Kit layout

When `--package-dir` is set:

```
sovereign-kit/
├── BUNDLE_MANIFEST.json      # cryptographic bundle root
├── attest.json               # primary attestation (product artifact)
├── attest.md                 # human summary (pandoc → attest.pdf)
├── health_certificate_v2.json
├── spec_v4.json
├── ledger.jsonl
├── zkap_attestation.json
├── archovive-cli/            # logical component markers
├── archovive-core/
├── archovive-runtime/
├── archovive-audit/
├── archovive-health/
├── archovive-spec/
└── archovive-attestation/
```

`BUNDLE_MANIFEST.json` binds artifact hashes and `bundle_hash`.

## 2. Product experience

### 2.1 Sovereign bootstrap (~60s)

Standalone:

```bash
archovive bootstrap
archovive bootstrap --json   # single-line JSON for CI
```

TTY ends with `BOOTSTRAP: PASS` or `BOOTSTRAP: FAIL`. Also runs at the start of `archovive analyze` (skip with `--no-bootstrap`).

Programmatic: `archovive_os.product_v1.run_bootstrap()`.

### 2.2 Truth simulator (5 minutes)

```bash
archovive simulate              # full walkthrough (TTY)
archovive simulate --pause      # step-by-step (Press Enter)
archovive simulate --json       # CI / automation
```

Five live steps on golden `pipe_l3_dora_violation`:

1. **Ingestion** (L1) — `H_input`, `H_triangulation`, `H_verdict`
2. **Runtime** (L2) — ledger, epoch binding, hypervisor binding, ZKAP
3. **Governance** (L3) — `NON_COMPLIANT`, `ICS-01` / `dora_ics_capacity`
4. **Attestation** — sovereign `attestation_hash` + trust surface
5. **Replay** — bit-identical golden reproduction

Ends with `SIMULATE: PASS` when verdict and replay match the fixture.

For a full kit after the demo:

```bash
archovive analyze archovive_os/golden/pipe_l3_dora_violation/input.json \
  --out attest.json --package-dir ./demo-kit
```

### 2.3 Attestation package

| Artifact | Source |
|----------|--------|
| `attest.json` | v1 attestation schema |
| `attest.md` / `attest.pdf` | `archovive attestation export attest.json --pdf` |
| `ledger.jsonl` | L3 audit ledger |
| `zkap_attestation.json` | L2 ZKAP |
| `health_certificate_v2.json` | Post-analyze integrity |
| `spec_v4.json` | PIPE_V4_SPEC document |
| Binding hashes | `trust_surface` in attest.json |

## 3. Product trust layer

| Layer | v1 name | v4 engine |
|-------|---------|-----------|
| Constitution | SPEC v4 | `PIPE_V4_SPEC` / `archovive pipe-spec` |
| TÜV seal | Health Certificate v2 | `archovive pipe-health-certificate` |
| Reproducibility | Golden Replay Matrix | `archovive pipe-replay` + CI |

**Replay** (unchanged, bit-identical):

```bash
archovive pipe-replay pipe_l3/dora_critical
```

## 4. CTO / CISO journey

| Step | Action | Time |
|------|--------|------|
| Install | `pip install -e archovive_os` + `archovive doctor` | ~1 min |
| Demo | `archovive analyze . --out attest.json --package-dir kit` | ~5 min |
| Attestation | Ship `attest.json` + `BUNDLE_MANIFEST.json` | — |
| Replay | `archovive pipe-replay <fixture>` | seconds |
| Assurance | `health_certificate_v2.json` + `spec_v4.json` | — |

## 5. Compatibility

- Pipe v4.0 public APIs (`run_pipe`, `run_runtime_pipe`, `run_audit_pipe`) are **unchanged**.
- `archovive pipe`, `pipe-runtime`, `pipe-audit` remain available for power users.
- v1 adds **additive** CLI (`analyze`) and `product_v1` module only.

## 6. Repository hygiene

- **`.gitignore`:** monorepo root `gov/.gitignore` — sovereign kits, attestations, ledgers, manifests, runtime caches, keys.
- **Open-core model:** [ARCHOVIVE_OPEN_CORE_MODEL.md](./ARCHOVIVE_OPEN_CORE_MODEL.md) — public product repo vs private `archovive-core`.

Never commit generated `sovereign-kit/`, `attest.json`, or `BUNDLE_MANIFEST.json`; ship them to customers out-of-band.

### 2.4 PDF export (auditor package)

```bash
archovive attestation export attest.json --pdf
archovive attestation export attest.json --pdf --out ./kit/attest.pdf
archovive attestation export attest.json --md-only
archovive attestation export attest.json --json
```

Deterministic pipeline: fixed `SOURCE_DATE_EPOCH`, pandoc metadata, LaTeX `lmodern` via template variables. Requires `pandoc` + `pdflatex` on PATH for PDF.

`archovive analyze --package-dir` writes `attest.md` and attempts `attest.pdf` when pandoc is available.

## 7. Roadmap (next)

| Block | Status |
|-------|--------|
| `archovive bootstrap` | Done |
| `archovive simulate` | Done |
| PDF exporter (`archovive attestation export`) | Done |
| Multi-binary Sovereign Kit (`archovive-cli` … `archovive-attestation`) | Done |

## 8. Implementation map

| Vision component | Code |
|------------------|------|
| `archovive analyze` | `archovive_os/cli/analyze_cli.py` |
| `archovive bootstrap` | `archovive_os/cli/bootstrap_cli.py` |
| `archovive simulate` | `archovive_os/cli/simulate_cli.py` |
| `archovive attestation export` | `archovive_os/cli/attestation_export_cli.py` |
| PDF / Markdown export | `archovive_os/product_v1/attestation_export.py` |
| Attestation builder | `archovive_os/product_v1/analyze.py` |
| Truth Simulator | `archovive_os/product_v1/simulate.py` |
| Sovereign bootstrap | `archovive_os/product_v1/bootstrap.py` |
| BUNDLE_MANIFEST | `archovive_os/product_v1/bundle.py` |
