# demo-fintech — Deterministic Reference Fixture

**Regression anchor for OSS pins and DGPP** — not a domain scope, surface, tier, or capability.

## The story (pedagogy only)

**NovaPay** is a fictional European payments API — narrative context for learning, **not** production code or proof of fintech-only applicability.

The repo encodes **intentional layer-boundary violations** — the pattern that fails DORA audits and release gates. Archovive scans this fixture in seconds and materializes a policy verdict with replay hash.

See gate output in the [README](../../README.md#try-it). Run `make demo` or `archovive simulate --verbose` for per-rule detail.

→ [Reference fixtures spec](../../specs/07_reference_fixtures.md) · [examples index](../README.md)

---

## 3 intentional anti-patterns (in code)

| # | Where | What | What the OSS gate shows |
|---|-------|------|-------------------------|
| 1 | `services/api/routes.py` | API imports `payments.ledger` directly | **DORA_2026** boundary crossing → `POLICY_VIOLATION` |
| 2 | `services/api/routes.py` | API calls `payments.processor.run_batch` | Layer mixing (visible in graph metrics) |
| 3 | `services/payments/ledger.py` | Ledger calls `notify_ops` inline | Critical-domain coupling (code smell) |

The default gate surfaces violation **#1** as the blocking rule. Rules **GLOBAL_BASE** and **NIS2_MINIMAL_V1** pass on this fixture.

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

Expected verdict: `POLICY_VIOLATION` · gate exit code **2** · hashes pinned in [`simulate/format.py`](../../simulate/format.py)

---

## What you learn

- **Drift** alone is not enough — first run has `drift_status: unmeasured` (neutral, not a risk signal)
- **Policy** fires on graph metrics — the DORA rule fails because `boundary_crossings > 0`
- **CI** must use `ci check` so the process exit code blocks the merge → [ch-03 CI](../../docs/integrate/ch-03-ci.md)

Pilot on **your** repository: [pricing](../../docs/evaluate/pricing.md#pilot-program) · **pilot@archovive.com**
