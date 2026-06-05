# 07 — Enterprise

## Wann du Enterprise brauchst

- Eigene Repositories (nicht nur Demo)
- `archovive run`, `gate`, `governance decide`
- Signierte Lizenz, Live-Dispatch, Multi-Repo

## Install

1. GitHub Release **v5.0.0** — ZIP + `.sha256` + SLSA
2. `bash internal/install_archovive.sh`
3. `source archovive.env`
4. `./archovive-enterprise-5.0.0/scripts/setup_license.sh --system`

## Frameworks

| Pack | Regulierung |
|------|-------------|
| DORA_2026 | Digital Operational Resilience |
| NIS2_MINIMAL_V1 | Cyber Security |
| CRA_MINIMAL_V1 | Cyber Resilience Act |
| SOX_2026 | ITGC |

## Sidecar & Audit

- XDG: Config, Cache, State getrennt vom Bundle
- Transparency Log, Vault Store
- SIEM-Export (Enterprise)

Engine-Quellcode: **Archovive-core** (Commercial) — `enterprise@archovive.com`

→ [08 — Pricing](../08-pricing/README.md)
