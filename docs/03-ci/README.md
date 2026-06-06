# Chapter 03 — CI gate

## Who is this chapter for?

**Platform engineers, DevOps, and release managers** who want objective merge blockers — exit codes instead of Slack debates, drift and policy **before** merge, not after an incident.

**Surface sold:** `archovive ci check` (OSS demo) → full pipeline gate with `repro.json` + drift matrix (Team/ci) → signed attestation upload (Enterprise/gov).

---

## The CI problem

Most pipelines check:

- Unit tests ✓
- Lint ✓
- SAST (line bugs) ✓

What's missing: **architecture governance.**  
Nobody blocks the merge when the API suddenly imports payment-ledger internals — until the auditor or a production incident.

Archovive closes that gap with **deterministic exit codes**.

<p align="center"><img src="../../assets/gifs/ci.gif" alt="CI gate — archovive ci check" width="600"></p>

---

## The gate command

```bash
archovive ci check
```

| Exit code | Meaning | CI action |
|-----------|---------|-----------|
| **0** | All policies passed | Allow merge |
| **1** | Drift violation | Block merge |
| **2** | Policy / regulatory violation | Block merge |
| **3** | Engine error | Red pipeline, investigate |
| **4** | Misuse / missing args | Fix pipeline config |

On the **OSS demo repo**, exit **2** is expected (DORA boundary crossing) — proof your pipeline actually stops on violations.

`simulate` prints the same gate lines but exits **0**; only **`ci check`** propagates the gate exit code to the shell.

Local demo: `bash docs/assets/demo/ci_gate.sh`

---

## GitHub Actions — full example

```yaml
name: archovive-governance
on:
  pull_request:
    branches: [main]

jobs:
  architecture-gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install Archovive OSS
        run: pip install -e internal/

      - name: Architecture & policy gate
        run: |
          export PATH="$PWD/dist:$PATH"
          archovive ci check --repo examples/demo-fintech
        # Demo: exit 2 expected. Production: remove --repo, use enterprise bundle.

      - name: Upload evidence JSON
        if: always()
        run: |
          export PATH="$PWD/dist:$PATH"
          archovive simulate --json > archovive-evidence.json

      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: archovive-evidence
          path: archovive-evidence.json
```

---

## Production CI (enterprise bundle)

With the enterprise bundle on **your** repository:

```yaml
      - name: Archovive full analysis
        run: |
          source archovive.env
          archovive run
          archovive verify attestation.json
```

Upload artifacts (`repro.json`, `drift_matrix.json`, `attestation.json`) as pipeline artifacts → audit trail without manual export.

**MCP in CI:** use CLI in pipelines; use MCP (`archovive.run_analysis`) in the IDE for the same kernel truth.

---

## Reproducibility in CI

Archovive's **functional SLA** (not a latency SLA):

> Same commit + same policy packs → same `replay_hash` on every runner.

CI results are **comparable** across developer laptop, GitHub Actions, and on-prem runners — no "works on my machine" governance.

---

## Transition to governance

OSS `ci check` uses simplified policy rules on the demo graph. Enterprise adds:

- Full policy packs (DORA, NIS2, CRA, SOX) with Ed25519 `.json.sig` signatures
- Signed attestations
- Drift vs stored baseline
- Transparency log

→ [Chapter 04 — Governance](../04-governance/README.md)

---

**Next chapter:** [04 — Governance](../04-governance/README.md) — policies, drift matrix, and verdicts in detail.
