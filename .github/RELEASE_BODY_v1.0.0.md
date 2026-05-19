# Archovive v1.0.0 — Deterministic Architecture Governance

Archovive v1.0.0 ist der erste öffentliche Release der souveränen Produktoberfläche.  
Er enthält die vollständige CLI-Suite, die Self-Attestation-Pipeline, den DORA-Walkthrough und den auditor-fähigen PDF-Exporter — alles ohne Core-IP.

## What's included

- **archovive-cli** — Produktoberfläche
- **bootstrap** — Self-Attestation
- **simulate** — DORA-Golden-Walkthrough
- **analyze** — Sovereign Attestation Package
- **attestation export** — auditor-fähiges PDF
- **Binary Suite** — 7 Binaries, eine Engine
- **SPEC v4 Schema** · **Health Certificate v2 Schema**
- **Demo-Fixtures** (synthetisch)
- **Open-Core Dokumentation**

## Sovereign Kit Output

```
sovereign-kit/
├── attest.json
├── attest.md
├── attest.pdf
├── health_certificate_v2.json
├── spec_v4.json
├── ledger.jsonl
└── zkap_attestation.json
```

## Open-Core Model

| Repository | License | Contents |
|------------|---------|----------|
| **archovive** (this repo) | MIT | CLI, Produktoberfläche, Docs |
| **archovive-core** | Commercial | Engine, Hypergraph, Policies, Proof-Pipeline, Golden-Fixtures |

**Core-Access:** core@archovive.com

## Documentation

- [Product Overview](docs/ARCHOVIVE_PRODUCT_OVERVIEW.md)
- [Sovereign Spec v1](docs/ARCHOVIVE_SOVEREIGN_SPEC_V1.md)
- [Binary Suite](docs/ARCHOVIVE_BINARY_SUITE.md)
- [Open-Core Model](docs/ARCHOVIVE_OPEN_CORE_MODEL.md)
- [Release Notes](docs/RELEASE_NOTES_v1.0.0.md)

## The first sovereign verdict

Archovive attests to itself before it attests to anything else.

```bash
archovive bootstrap
archovive simulate
archovive analyze . --out attest.json
archovive-attestation export attest.json --pdf
```

**Requires:** `archovive-core` from private registry.
