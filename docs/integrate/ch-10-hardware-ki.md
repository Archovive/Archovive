# ch-10 — Hardware-KI integration (bundle appliance)

**Integrate** · [README](../../README.md) · [Docs](../README.md) · [Evaluate](../evaluate/decision-hub.md) · [← ch-09 MCP](ch-09-mcp.md)

**Bundle appliance only** — no OSS demo path. Semantics → [specs/03_attestation_schema.md](../../specs/03_attestation_schema.md) · [specs/00_kernel_truth_model.md](../../specs/00_kernel_truth_model.md#exit-code-mapping-kernel-derived) · [ch-06 Air-gap](ch-06-airgap.md)

---

## Intent

Run Archovive on a **hardware-KI appliance**: read-only bundle under `/opt/archovive`, repository and evidence on sidecar mounts, deterministic JSON outputs for KI interpretation. Offline, no telemetry.

---

## Function

### 1. Runtime (bundle profile)

```bash
export ARCHOVIVE_ISOLATED=1
export PATH="/opt/archovive/bin:${PATH}"
```

| Path / variable | Role |
|-----------------|------|
| `/opt/archovive` | Read-only bundle mount (PyInstaller — **no Python required**) |
| `/etc/archovive/archovive_license.json` | Ed25519 license (fail-closed) |
| `/workspace/repo` | Repository mount → `ARCHOVIVE_REPO` |
| `/workspace/evidence` | Evidence sidecar mount → `ARCHOVIVE_STATE` |

```bash
export ARCHOVIVE_REPO=/workspace/repo
export ARCHOVIVE_STATE=/workspace/evidence
```

Do **not** write into `/opt/archovive`. Sidecar layout → [ch-06 Air-gap](ch-06-airgap.md).

### 2. Installation

```bash
# 1. Verify release (hashes + signature) — see ch-06
# 2. Unpack bundle to read-only mount
install -d /opt/archovive
# … unpack archovive-enterprise-*.zip contents to /opt/archovive …

# 3. Bundle installer (not repo internal/install_archovive.sh)
/opt/archovive/scripts/install.sh

# 4. License (system)
/opt/archovive/scripts/setup_license.sh --system
# → /etc/archovive/archovive_license.json

# 5. CLI on PATH
ln -sf /opt/archovive/bin/archovive /usr/local/bin/archovive

# 6. Appliance mounts
install -d /workspace/repo /workspace/evidence
```

### 3. KI runtime commands

**Merge gate (enforcement — process exit = kernel exit_code):**

```bash
archovive ci check --repo /workspace/repo
echo $? > /workspace/evidence/exit_code
```

**Full pipeline + evidence writes (bundle):**

```bash
archovive run --repo /workspace/repo
archovive evidence --repo /workspace/repo
```

Optional JSON capture:

```bash
archovive ci check --repo /workspace/repo --json > /workspace/evidence/out.json
```

Use **`ci check`** for gate semantics. Do not use OSS `simulate` funnel on the appliance.

### 4. Outputs (write to `/workspace/evidence` only)

| Artifact | Role |
|----------|------|
| `repro.json` | Canonical replay record |
| `attestation.json` | Gov-tier signed certificate |
| `evidence/` | Kernel serializations from `run` / export |
| `replay_hash` | Cross-surface decision identity (inside JSON) |

Schema → [specs/03_attestation_schema.md](../../specs/03_attestation_schema.md) · [`schemas/repro.json`](../../schemas/repro.json)

### 5. CI hook (appliance)

```bash
#!/bin/sh
set -e
archovive ci check --repo /workspace/repo
code=$?
echo "$code" > /workspace/evidence/exit_code
exit "$code"
```

### 6. Appliance tests

| Test | Pass criteria |
|------|----------------|
| `archovive doctor` | Bundle health OK |
| Real repo run | `archovive run --repo /workspace/repo` completes |
| Replay record | `repro.json` present; `replay_hash` stable across re-run |
| Parallel determinism | 10× identical job → identical `replay_hash` |
| Policy violation | Known-bad repo → process exit **2** via `ci check` |

Do **not** use `make demo` / `make ci-demo` on the appliance — those are OSS fixture tests only.

### 7. KI prompts (mapping)

| Prompt | Action |
|--------|--------|
| "run archovive" | `archovive ci check --repo /workspace/repo` or `archovive run --repo /workspace/repo` |
| "show drift" | Read `drift_matrix` from `repro.json` (requires baseline — Team+) |
| "give evidence" | List `/workspace/evidence/` — `repro.json`, `attestation.json`, exports |

KI **interprets** artifacts; it does not redefine kernel semantics.

### 8. End-to-end

```text
repo mount (/workspace/repo)
  → archovive ci check
  → repro.json (+ attestation.json on gov tier)
  → replay_hash stable
  → KI reads JSON → report
```

---

## Truth (references — do not redefine here)

| Topic | Spec |
|-------|------|
| Exit codes 0–4 | [Kernel truth model § Exit code mapping](../../specs/00_kernel_truth_model.md#exit-code-mapping-kernel-derived) |
| `repro.json` / `attestation.json` | [Attestation schema](../../specs/03_attestation_schema.md) |
| Determinism / job envelope | [Invariants](../../specs/05_invariants_and_determinism.md) · [Kernel contract](../../specs/06_kernel_contract_v1.md) |
| Sidecar / isolated mode | [ch-06 Air-gap](ch-06-airgap.md) |

**Exit codes (kernel truth model):**

| Code | Meaning |
|------|---------|
| 0 | Allow |
| 1 | Drift |
| 2 | Policy violation |
| 3 | Engine error |
| 4 | Misuse / invalid invocation |

**Determinism invariants:** identical job envelope → identical `replay_hash`; no writes to `/opt/archovive`; kernel job contains no tier/surface fields.

---

[← ch-09 MCP](ch-09-mcp.md) · [Air-gap](ch-06-airgap.md) · [Evidence procedures](ch-05-evidence.md)
