# demo-fintech — Lern-Repository für Archovive Simulate

## Die Story

**NovaPay** ist eine fiktive europäische Payments-API — kein Produktionscode, sondern ein **Absichts-Beispiel** für Architektur-Governance.

Das Team hat schnell gebaut: API-Routes, Payment-Ledger, Batch-Processor, Ops-Notifications. Alles funktioniert in Tests. Aber die **Schichtgrenzen** wurden nie durchgesetzt — genau das Muster, das bei DORA-Audits und Release-Gates auffliegt.

Archovive scannt dieses Repo in ~30 Sekunden und zeigt dir, **warum** ein Release blockiert würde — nicht als Meinung, sondern als Policy-Verdict mit Replay-Hash.

---

## 3 absichtliche Verstöße (eingebaut)

| # | Wo | Was | Policy |
|---|-----|-----|--------|
| 1 | `services/api/routes.py` | API importiert `payments.ledger` direkt | **DORA_2026** — layer boundary breach |
| 2 | `services/api/routes.py` | API ruft `payments.processor.run_batch` auf | Schichtvermischung / critical-path |
| 3 | `services/payments/ledger.py` | Ledger triggert Notifications inline | Kopplung kritischer Domains |

Du musst den Code nicht lesen, um das Problem zu verstehen — `archovive simulate` erklärt es dir.

---

## Struktur

```text
services/api/              HTTP-Schicht (sollte nicht in Ledger greifen)
services/payments/         Zahlungsdomäne — Ledger, Processor
services/notifications/    Ops-Alerts
shared/                    Config & Audit-Logging
tests/                     Smoke-Test (grün — Architektur trotzdem rot)
```

**12 Module.** Klein genug zum Scrollen, groß genug für realistische Metriken (`coupling_index`, `boundary_crossings`).

---

## Ausführen

```bash
archovive simulate
archovive simulate --repo examples/demo-fintech
archovive ci check --repo examples/demo-fintech   # Exit 2 — Merge würde blockieren
```

Erwarteter Verdict: `POLICY_VIOLATION` · Exit **2** · `replay_hash` gepinnt in [simulate/README.md](../../simulate/README.md)

---

## Was du daraus lernst

- **Drift** allein reicht nicht — beim ersten Lauf ist `drift_status: unmeasured` (neutral, kein Risiko-Signal)
- **Policy** feuert sofort — weil Regeln auf Graph-Metriken operieren, nicht auf „kenne ich diesen Code?"
- **CI** kann dasselbe automatisieren → [docs/03-ci](../../docs/03-ci/README.md)

Pilot auf **deinem** Repository: [docs/08-pricing](../../docs/08-pricing/README.md#pilotphase) · **pilot@archovive.com**
