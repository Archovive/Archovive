# Kapitel 05 — Evidence

## Für wen ist dieses Kapitel?

Für **Auditoren, IT-Compliance, CRA/NIS2-Verantwortliche und SIEM-Betreiber**, die **prüfbare Artefakte** brauchen — nicht Screenshots, nicht mündliche Bestätigungen, sondern signierte, replay-fähige Evidence Packs.

---

## Was ist ein Evidence Pack?

Ein Evidence Pack ist ein **zusammenhängendes Bündel** aus Analyse-Ergebnissen, das du an Prüfer, Regulatoren oder interne Revision weitergeben kannst:

| Datei | Inhalt | Tier |
|-------|--------|------|
| `ARCHOVIVE_OUTPUT.md` | Menschlicher Report | core+ |
| `repro.json` | Replay-Metadaten, Graph-Hashes | ci+ |
| `drift_matrix.json` | Drift-Taxonomie | ci+ |
| `compliance_report.json` | Policy-Pack-Matrizen | gov |
| `attestation.json` | Signierte Verdict-Bescheinigung | gov |
| `risk_matrix.json` | Risiko-Zeilen aus Analyse | gov |

OSS-Demo liefert Terminal/JSON. Enterprise-Bundle schreibt das volle Set ins Analyse-Verzeichnis.

---

## Attestations

`attestation.json` ist das **Kernstück für Auditoren**:

- `H_verdict` — Hash der Entscheidung
- `trust_surface` — Verkettung: audit_chain_root, epoch_binding, hypervisor_binding
- Ed25519-Signatur (gov-Tier)
- Decision Trace — welche Policy-Regeln feuerten

**Verify ohne Re-Analyse:**

```bash
archovive verify attestation.json
```

Trustless: Dritte können die Bescheinigung prüfen, ohne dein Repository erneut zu scannen.

---

## SBOM & Supply Chain

Archovive erzeugt SBOM-Daten mit **`file_hashes`** — SHA-256 pro Dateipfad im Analyse-Scope. Relevant für:

- **CRA** — Software-Transparenz für digitale Produkte
- **NIS2** — Lieferketten-Nachweise
- **DORA** — ICT-Risikomanagement
- **SLSA** — Build-Provenance

Leere `file_hashes` im gov-Tier = Bug, kein Feature.

---

## SLSA & Build-Provenance

Das Enterprise-Release liefert:

| Artefakt | Zweck |
|----------|--------|
| `archovive.slsa.provenance.json` | SLSA v1 — wer, wann, womit gebaut |
| `build_manifest.json` | SHA-256 jeder Datei im Bundle (~940 Pfade) |
| `archovive-enterprise-5.0.0.zip.sha256` | Release-Pin |
| cosign-Signaturen | Keyless Signing des CLI-Binaries |

Verify vor Installation:

```bash
sha256sum -c internal/releases/archovive-enterprise-5.0.0.zip.sha256
./archovive-enterprise-5.0.0/scripts/verify_signature.sh
```

*(Hashes liegen in `internal/releases/` — Build-Pin, nicht Endnutzer-Dokumentation.)*

---

## Signaturen

| Was | Algorithmus | Wo |
|-----|-------------|-----|
| Policy Packs | Ed25519 (`.json.sig`) | Enterprise-Bundle |
| Enterprise-Lizenz | Ed25519 | `archovive_license.json` |
| Attestation | Ed25519 | `attestation.json` |
| CLI-Binary | cosign (keyless) | GitHub Release |

Enterprise **fail-closed**: ohne gültige Lizenz-Signatur kein gov-Tier, kein Live-Dispatch.

---

## Evidence Camera (Enterprise)

```bash
archovive evidence
archovive camera evidence
```

MCP-Äquivalent: `archovive.evidence`, `archovive.global`

Benchmark-JSON (Flask, FastAPI, Django) im Bundle für globale Vergleichsmatrizen — `global_matrix.json`, `global_ranking.json`.

---

## Audit-Kanal

Wirtschaftsprüfer und GRC-Boutiquen können Evidence Packs **pro Repository / pro Release** archivieren — deterministisch, wiederholbar, ohne erneute Analyse-Kosten.

Indikativer Enterprise-Preis: **€2.500 / zertifiziertes Repository / Jahr** → [Kapitel 08](../08-pricing/README.md)

---

**Nächstes Kapitel:** [06 — Air-gap](../06-airgap/README.md) — Offline-Betrieb ohne Cloud und ohne Telemetry.
