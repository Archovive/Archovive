# Demo-Fintech — OSS Simulate Fixture

Absichtlich fehlerhafte Microservice-Struktur für `archovive simulate`.

## Struktur

```
services/api/           HTTP-Schicht
services/payments/      Zahlungsdomäne (Ledger, Processor)
services/notifications/ Ops-Benachrichtigungen
shared/                 Config & Logging
tests/                  Smoke-Test
```

## Der absichtliche Verstoß

`services/api/routes.py` importiert `payments.ledger` direkt — die API-Schicht sollte nicht auf Ledger-Interna zugreifen. Das triggert **DORA_2026 :: dora_crossings_max**.

## Ausführen

```bash
archovive simulate
archovive simulate --repo examples/demo-fintech
archovive ci check --repo examples/demo-fintech   # Exit 2
```

Dokumentation: [docs/02-simulate/README.md](../../docs/02-simulate/README.md)
