# Archovive v1.0.0 — Release Notes

**Tag:** `v1.0.0`  
**Title:** Archovive v1.0.0 — Deterministic Architecture Governance  
**Type:** Stable

---

## GitHub Release Body (copy-paste)

```markdown
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
```

---

## Ship checklist

### Pre-tag (monorepo / split tree)

- [ ] `bash scripts/release_gate_v1.sh` → `RELEASE_GATE: PASS`
- [ ] `bash scripts/split_archovive_repos.sh` → Repo A Soll-Struktur
- [ ] `bash scripts/cleanup_repo_a.sh ../split/archovive` → `CLEANUP: PASS`
- [ ] `bash archovive_os/scripts/verify_repo_a_boundary.sh ../split/archovive` → `BOUNDARY: PASS`

### Tag (Repo A public remote)

```bash
git tag -a v1.0.0 -m "Archovive v1.0.0 — Deterministic Architecture Governance"
git push origin v1.0.0
```

### GitHub Release

```bash
gh release create v1.0.0 \
  --title "Archovive v1.0.0 — Deterministic Architecture Governance" \
  --notes-file archovive_os/docs/RELEASE_NOTES_v1.0.0.md
```

Or paste the **GitHub Release Body** block above in the GitHub UI.

### Repo B (private)

- [ ] Wheel `archovive-core==4.0.0` on private index
- [ ] Tag `archovive-core-4.0.0`

---

## Release gate results

| Check | Expected |
|-------|----------|
| Boundary | `BOUNDARY: PASS` |
| Cleanup | `CLEANUP: PASS` |
| Product tests | 33+ passed |
| bootstrap | `BOOTSTRAP: PASS` |
| simulate | `SIMULATE: PASS`, `replay_match` |
| analyze | `attest.json` written |
| attestation export | `PASS` |
| PDF | `PASS` if pandoc installed |
