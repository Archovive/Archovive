# SBOM semantics

SBOM evidence is produced by the **product bundle engine** (polyglot IR + CycloneDX-style BOM).

## `file_hashes`

Map: **repo-relative path → SHA-256** of file content.

- Populated from polyglot IR (`content_hash` / `sha256` per file).
- Empty values are a **bug**, not a first-run or baseline effect.
- Required for supply-chain attestations (CRA, NIS2, DORA, SLSA-style audits).

## CLI

```bash
archovive sbom [--out=PATH]
```

(requires installed bundle)

## Evidence JSON

Benchmark `sbom.json` includes `sbom_hash`, `ir_hash`, and `file_hashes` (pilot ZIP under `benchmarks/`).
