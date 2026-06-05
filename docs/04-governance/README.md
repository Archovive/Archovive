# 04 — Governance & Evidence

## Was du bekommst (Enterprise)

| Artefakt | Zweck |
|----------|--------|
| `compliance_report.json` | Policy-Pack-Auswertung (DORA, NIS2, CRA, SOX) |
| `attestation.json` | Signierte Release-Bescheinigung |
| `repro.json` | Replay-Metadaten, Graph-Hashes |
| `drift_matrix.json` | Strukturelle Abweichung gegen Baseline |

## Policy Packs

Regulatorische Regeln als Graph-Invarianten — nicht als Checklisten.

Im OSS-Demo: `GLOBAL_BASE`, `DORA_2026`, `NIS2_MINIMAL_V1`.  
Vollständige Packs & Signaturen: Enterprise-Bundle (`internal/policy_packs/` im Build).

## Verify

```bash
archovive verify attestation.json
```

Trustless — ohne erneute Analyse.

## SLSA & Supply Chain

Enterprise-Release liefert:

- `archovive.slsa.provenance.json`
- cosign-Signaturen
- `build_manifest.json` (per-Datei SHA-256)

→ [06 — Air-gap](../06-airgap/README.md) · [07 — Enterprise](../07-enterprise/README.md)
