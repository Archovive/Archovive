# Archovive Enterprise 5.0.0 — Release Notes

**Release date:** 2026-06-05  
**Bundle:** `archovive-enterprise-5.0.0.zip`  
**Schema:** `archovive_product_bundle_v3`

## Checksums

| Artifact | SHA256 |
|----------|--------|
| `archovive-enterprise-5.0.0.zip` | `07c99c1e07f7656ddba5947ca8e53bc245c462426fe616371acdaa538531fc33` |
| CLI binary (`libexec/archovive/archovive`) | `ced22f46cf573b4d971648852a70fc4f6bbe6e887794175d7304a2eda8516ef4` |

SLSA provenance: `metadata/archovive.slsa.provenance.json` (inside bundle)

## Bundle contents

```text
archovive-enterprise-5.0.0/
├── bin/           archovive, archovive-mcp (XDG-aware wrappers)
├── libexec/       PyInstaller runtime (read-only)
├── share/
│   ├── docs/      README, COMMAND_LIBRARY, TROUBLESHOOTING, SECURITY, CHANGELOG
│   ├── legal/     LICENSE, COPYRIGHT, THIRD_PARTY_NOTICES, archovive_license.json
│   ├── examples/  governance, baseline, drift, compiler spec
│   └── templates/ env template, systemd units, policy packs
├── scripts/       install.sh, verify_signature.sh, setup_license.sh
└── metadata/      build_manifest.json, sha256.txt, slsa provenance
```

## System requirements

- Linux x86_64 (glibc 2.31+)
- Python **not** required (frozen offline binaries)
- `unzip` for initial unpack
- Optional: systemd for MCP sidecar template

## Installation

```bash
unzip archovive-enterprise-5.0.0.zip
cd archovive-enterprise-5.0.0
sudo ./scripts/install.sh          # default: /opt/archovive-enterprise-5.0.0
./scripts/verify_signature.sh
./scripts/setup_license.sh
source /etc/archovive/archovive.env
archovive --version
archovive doctor
```

Open-core installer (public repo): `./install_archovive.sh` with ZIP in repo root.

## Determinism matrix (frozen)

E2E django enterprise, frozen binary, Run 1 = Run 2:

| Signal | Hash (prefix) |
|--------|----------------|
| `baseline_hash` | `4518a790…` |
| `drift_matrix_hash` | `bf0d1c94…` |
| `decision_hash` (ask = chat = governance) | `25bb23a8…` |

## Truth surfaces

`archovive ask`, `archovive chat`, and `archovive governance decide` share identical `decision_hash` and `risk_level` for the same repo state.

## Breaking changes (v4 → v5)

- Bundle root renamed: `archovive/` → `archovive-enterprise-5.0.0/`
- Binaries under `bin/` (wrappers), not bundle root
- License at `share/legal/archovive_license.json` (use `setup_license.sh` for XDG config)
- `ARCHOVIVE_ENGINE_ROOT` deprecated → `ARCHOVIVE_BUNDLE_ROOT`
- Manifest at `metadata/build_manifest.json` (v3 schema)

## Known issues

- Policy packs must be copied to `$ARCHOVIVE_CONFIG/policy_packs/` on first install (`doctor` may exit 1 until configured).
- MCP systemd unit uses stdio bridge — site policy may require socket activation.

## Support

enterprise@archovive.com | security@archovive.com
