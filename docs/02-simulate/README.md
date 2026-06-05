# 02 — In 30 Sekunden testen

## Install

```bash
bash dist/install.sh
```

Oder manuell:

```bash
pip install -e internal/
export PATH="$PWD/dist:$PATH"
```

## Demo ausführen

```bash
archovive simulate
```

### Erwartete Ausgabe (v5.0.0, Demo-Repo `examples/demo-fintech`)

```
=== Archovive Simulate (OSS demo) ===
Version .............. 5.0.0
Repository ............. demo-fintech
Modules .............. 12

[1/4] Architecture graph
  graph_hash ........... fee879ce6ea2d296…
  coupling_index ....... 0.833
  boundary_crossings ... 1

[2/4] Drift matrix
  drift_status ......... unmeasured
  drift_score .......... None

[3/4] Policy evaluation
  [PASS] GLOBAL_BASE :: global_coupling_max
  [FAIL] DORA_2026 :: dora_crossings_max
  [PASS] NIS2_MINIMAL_V1 :: nis2_instability_ceiling

[4/4] Verdict
  verdict .............. POLICY_VIOLATION
  replay_hash .......... 3e700b6addb40128…
  exit_code ............ 2
```

Das Demo-Repo ist eine **absichtlich fehlerhafte** Fintech-Microservice-Struktur: die API-Schicht greift direkt auf `payments.ledger` zu — ein DORA-Grenzverstoß.

## JSON

```bash
archovive simulate --json
```

## Eigenes Repo (OSS)

```bash
archovive simulate --repo path/to/your-repo
```

Für produktive Analyse auf echten Repositories → [07 — Enterprise](../07-enterprise/README.md).

→ [03 — CI](../03-ci/README.md)
