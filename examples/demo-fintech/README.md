# demo-fintech — learning repository for Archovive simulate

## The story

**NovaPay** is a fictional European payments API — not production code, but an **intentional example** for architecture governance.

The team shipped fast: API routes, payment ledger, batch processor, ops notifications. Tests pass. But **layer boundaries** were never enforced — exactly the pattern that fails DORA audits and release gates.

Archovive scans this repo in a few seconds and shows **why** a release would be blocked — not as opinion, but as a policy verdict with replay hash.

See the gate output in the [README](../../README.md#what-you-get). Run `archovive simulate --verbose` for graph metrics and per-rule evaluation.

---

## 3 intentional anti-patterns (in code)

| # | Where | What | What the OSS gate shows |
|---|-------|------|-------------------------|
| 1 | `services/api/routes.py` | API imports `payments.ledger` directly | **DORA_2026** boundary crossing → `POLICY_VIOLATION` |
| 2 | `services/api/routes.py` | API calls `payments.processor.run_batch` | Layer mixing (visible in graph metrics) |
| 3 | `services/payments/ledger.py` | Ledger calls `notify_ops` inline | Critical-domain coupling (code smell) |

The default gate surfaces violation **#1** as the blocking rule. Rules **GLOBAL_BASE** and **NIS2_MINIMAL_V1** pass on this demo.

---

## Structure

```text
services/api/              HTTP layer (should not touch ledger)
services/payments/         Payments domain — ledger, processor
services/notifications/    Ops alerts
shared/                    Config & audit logging
tests/                     Smoke test (green — architecture still red)
```

**12 modules.** Small enough to scroll, large enough for realistic metrics (`coupling_index`, `boundary_crossings`).

---

## Run

```bash
archovive simulate
archovive simulate --verbose
archovive simulate --repo examples/demo-fintech
archovive ci check --repo examples/demo-fintech   # process exit 2 — merge would block
```

Expected verdict: `POLICY_VIOLATION` · gate exit code **2** · `replay_hash` pinned in [simulate/README.md](../../simulate/README.md)

---

## What you learn

- **Drift** alone is not enough — first run has `drift_status: unmeasured` (neutral, not a risk signal)
- **Policy** fires on graph metrics — the DORA rule fails because `boundary_crossings > 0`
- **CI** must use `ci check` so the process exit code blocks the merge → [docs/03-ci](../../docs/03-ci/README.md)

Pilot on **your** repository: [docs/08-pricing](../../docs/08-pricing/README.md#pilot-program) · **pilot@archovive.com**
