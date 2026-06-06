# Chapter 02 — Simulate (30 seconds)

## Who is this chapter for?

**Developers, founders, and evaluators** who want to **see** Archovive — not believe a sales deck — without an enterprise contract, bundle download, or sales call.

---

## What happens when you run `simulate`?

Archovive analyzes the demo repository `examples/demo-fintech` — NovaPay, a fictional payments API with intentional layer violations. Analysis runs **locally** in a few seconds.

Default output = **product gate format** (identical to the [README](../../README.md#what-you-get)). With `--verbose` you see graph metrics, drift status, and all three evaluated policy rules (one fails on the demo: **DORA_2026**).

<p align="center"><img src="../../assets/gifs/gate.gif" alt="Gate output — archovive simulate" width="600"></p>

---

## Exit codes: `simulate` vs `ci check`

| Command | Prints gate exit code? | Process exit code |
|---------|------------------------|-------------------|
| `archovive simulate` | Yes (e.g. `Exit Code: 2`) | Always **0** — demo funnel |
| `archovive ci check` | Same gate output | **Matches gate** (0, 1, 2, …) — use in CI |

For merge blockers, use **`ci check`**, not `simulate`.

---

## Quickstart

### Option A — one-liner

```bash
git clone https://github.com/Archovive/Archovive.git
cd Archovive
bash dist/install.sh
```

### Option B — manual

```bash
pip install -e internal/
export PATH="$PWD/dist:$PATH"
archovive simulate
```

**Requirements:** Python 3.11+, Git recommended.

---

## Commands

```bash
archovive simulate              # Gate format (like README)
archovive simulate --verbose    # Graph, drift, policy rules
archovive simulate --json       # Machine-readable
archovive simulate --repo PATH  # Other repo
```

Bare `archovive` with no arguments also runs **simulate**.

---

## Why FAIL?

`services/api/routes.py` imports `payments.ledger` directly — layer boundary breach (`DORA_2026`). The demo repo contains **three intentional anti-patterns** in code; the OSS engine evaluates **three policy rules** and fails on the DORA boundary rule. See [examples/demo-fintech](../../examples/demo-fintech/README.md).

---

## Simulate vs enterprise `run`

| | **OSS `simulate`** | **Enterprise `run`** |
|---|---------------------|----------------------|
| Buyer | Evaluator | Platform / compliance |
| Surface | CLI only | CLI + MCP + CI artifacts |
| Repo | Demo or `--repo` | Any repository |
| Output | Gate format + optional `--verbose` | Full artifacts + attestation |
| Bundle required? | No | Yes |

---

**Next chapter:** [03 — CI](../03-ci/README.md) — wire simulate as a merge gate in GitHub Actions.
