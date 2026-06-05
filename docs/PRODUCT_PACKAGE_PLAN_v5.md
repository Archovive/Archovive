# Archovive Product Package — v5 Plan

**Status:** in progress (step 1 complete: core sync + binary)  
**Version:** 5.0.0 Enterprise stable

## Repositories

| Repo | Role | Sync script |
|------|------|-------------|
| **Archovive-core** (private) | Engine + kernel boundary + golden matrix | `scripts/sync_archovive_core_v5.sh` |
| **Archovive** (public) | Product package — installer, docs, tier profiles | `scripts/sync_archovive_product_v5.sh` |
| **archovive-os** (future) | Full runtime monorepo split | `repo_split/project_list.txt` |

## Phase 1 — Core release (now)

1. Sync engine from `packages/archovive_engine` → `archovive-core/archovive_engine`
2. Sync `decision_kernel/`, `golden/`, `schemas/` into core repo
3. Tag `v5.0.0` on Archovive-core
4. Attach binary + SLSA provenance to GitHub Release (not committed to git)

## Phase 2 — Product package (public) ✓ layout v3

Enterprise bundle structure (`archovive-enterprise-5.0.0/`):

```text
bin/           archovive, archovive-mcp (XDG-aware wrappers)
share/docs/    README, COMMAND_LIBRARY, TROUBLESHOOTING, SECURITY, CHANGELOG
share/legal/   LICENSE, COPYRIGHT, THIRD_PARTY_NOTICES, archovive_license.json
share/examples/ governance, baseline, drift, compiler spec
share/templates/ archovive.env.template, systemd/, policy_packs/
scripts/       install.sh, verify_signature.sh, setup_license.sh
metadata/      build_manifest.json, sha256.txt, archovive.slsa.provenance.json
libexec/       PyInstaller runtime payloads (immutable, not customer-edited)
```

1. Sync customer docs + deploy profiles → `Archovive` repo
2. Ship `install_archovive.sh` (v5 bundle unpack)
3. `RELEASE.lock.json` + `MANIFEST.json` with binary SHA256 pin
4. Customer drops `archovive-enterprise-5.0.0.zip` beside installer
5. Verify: `archovive --version`, `archovive doctor`, ask/chat/governance parity

## Phase 3 — Distribution automation

- [ ] GitHub Release workflow: core builds wheel + binary, product repo gets manifest bump
- [ ] Private PyPI index for `archovive-engine==5.0.0` (CI `ARCHOVIVE_CORE_PAT`)
- [ ] Cosign signing on release artifacts
- [ ] E2E matrix frozen hash published in release notes

## Phase 4 — Repo split completion

Gate before full monorepo split (`repo_split/manifest_v1.json`):

```bash
bash scripts/run_test_engine.sh
archovive-test-engine run --suite all
```

Then extract `archovive-os` per `project_list.txt`.

## v5.0.0 stable checklist

- [x] ask = chat = governance decide (truth bind)
- [x] Frozen binary feature-complete (waves 1–4, registry embedded)
- [x] Deterministic baseline/drift matrix (E2E Run 1 = Run 2)
- [x] Enterprise bundle export with advisories
- [ ] Core git tag `v5.0.0` pushed
- [ ] Product git tag `v5.0.0` pushed
- [ ] GitHub Release artifacts attached
