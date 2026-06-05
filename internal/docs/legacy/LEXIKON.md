# Archovive Lexikon

Kurzes technisches Glossar — ein Spine, drei Tiers. Tiefe: `archovive spec link <ID>`.

## Entscheidung

- **Gate** — `archovive gate` materialisiert eine Release-Entscheidung für das aktuelle Repo. Exit code 0/1/2/3. → `spec link Decision_Kernel`
- **Decision Contract** — JSON-Artefakt mit `decision_id`, `lookup_key`, `verdict`, Signatur. → `spec link Decision_Kernel`
- **lookup_key** — Stabiler Schlüssel für die Analyse-Oberfläche (CAS im Store).
- **verdict** — `APPROVED`, `REJECT`, `OVERRIDE_REQUIRED` — Produktstatus der Entscheidung.

## Wahrheit

- **kernel_truth_hash** — Fingerabdruck der Kernel-Wahrheit; invariant über Tiers.
- **spec_hash** — Hash des Capability-Spec (`spec/v1/`); Conformance-Pin.
- **artifact_identity_hash** — Bindung an Commit/Oberfläche/Policy.

## Produktschicht

- **Tier** — `personal` (6 Capabilities), `team` (12), `enterprise` (20). Env: `ARCHOVIVE_PRODUCT`. → `spec link Enterprise_Pricing`
- **Capability** — Atomare Berechtigung (z. B. `authoritative_store`, `mcp_read`). Aus `policy_vectors.json`.
- **Gate (team_surface)** — Authority gate für `archovive team *` (min tier: team).
- **Gate (authoritative_upload)** — Enterprise-Upload in den autoritativen Store.
- **Gate (live_enforcement)** — Live vendor dispatch (`act --live`).

## Operationalisierung

- **CGE** — Canonical Governance Event; Spine für Integration dispatch.
- **Dispatch** — Vendor-Ausführung (PagerDuty, Slack, Jira, GitHub). Enterprise default live.
- **Enforcement live** — `integration_live.default=enabled` für enterprise; Opt-out: `ARCHOVIVE_CONTROL_PLANE_LIVE=0`.
- **Admission** — Kubernetes/GitHub Checks-Bindung; explizit: `ARCHOVIVE_ADMISSION_ENABLED=1`.

## Identität & Audit

- **archovive_license.json** — `product_tier`, `pipeline_tier`, `entitlements`, Ed25519-Signatur (enterprise Pflicht).
- **Audit bundle** — `archovive audit export --bundle`; 6-Feld-Ledger. → `spec link Audit_Ledger`
- **SIEM export** — `GET /v1/product/ciso/siem-export` (enterprise).

## Tier-Matrix (Kurz)

| | Personal | Team | Enterprise |
|---|----------|------|------------|
| Lokales Gate | ja | ja | ja |
| Team feed | nein | ja | ja |
| Authoritative store | nein | nein | ja |
| Live dispatch | nein | nein | ja (default) |
| License-Signatur | optional | optional | **Pflicht** |

## CLI

| Befehl | Rolle |
|--------|-------|
| `archovive setup` | Tier, Key, License, optional Vendor-Keys |
| `archovive onboard` | Erste Entscheidung |
| `archovive ops runtime doctor` | Tier, Capabilities, Signatur, Vendor-Keys |
| `archovive bundle export --tier` | Offline-Produktpaket |
