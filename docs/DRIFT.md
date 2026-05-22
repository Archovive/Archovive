# Drift semantics

## No baseline (first run)

When no baseline exists for a repository:

| Field | Meaning |
|-------|---------|
| `drift_status: unmeasured` | Drift cannot be computed |
| `drift_score: null` | **Not** a risk indicator — neutral placeholder |
| `drift_reasons` | May list `*_drift_class=unmeasured` |

Do **not** read `null` as “medium risk”. A numeric score appears only after drift taxonomy is measured against a baseline.

## With baseline

Use `drift_matrix.json` in the analysis root and `drift_score` in evidence JSON when present.

## CLI / evidence

```bash
archovive evidence flask --json   # requires bundle; reads benchmarks/ or live run
```

See `docs/OUTPUTS.md` and `docs/CAMERAS.md`.
