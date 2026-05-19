# Archovive — Open-Core Model

Archovive ships as two repositories with different trust boundaries.

## Repo A — `archovive` (public, MIT)

**Purpose:** Product experience, CLI, and normative product documentation only.

### Soll-Struktur

```text
archovive/
├── README.md
├── LICENSE
├── pyproject.toml
├── setup.cfg
├── archovive_os/
│   ├── __init__.py
│   ├── cli/           # product entrypoints only
│   └── product_v1/    # analyze, bootstrap, simulate, export
└── docs/
    ├── ARCHOVIVE_PRODUCT_OVERVIEW.md
    ├── ARCHOVIVE_SOVEREIGN_SPEC_V1.md
    ├── ARCHOVIVE_BINARY_SUITE.md
    ├── ARCHOVIVE_OPEN_CORE_MODEL.md
    └── RELEASE_NOTES_v1.0.0.md
```

No enterprise docs, pipe docs, golden fixtures, engine sources, tests, or demo trees in Repo A.

### Allowlist

Exact paths: `repo_split/repoA_allowlist.txt`

### Build public tree

```bash
# From monorepo root (gov/)
bash scripts/split_archovive_repos.sh ../split/archovive ../split/archovive-core
bash scripts/cleanup_repo_a.sh ../split/archovive
bash archovive_os/scripts/verify_repo_a_boundary.sh ../split/archovive
```

## Repo B — `archovive-core` (private, commercial)

**Purpose:** Engine, Pipe v4 L1/L2/L3, golden matrix, generators, full CI.

Includes the full `archovive_os/` tree (pipe, runtime, audit, bridge, enterprise, internal docs under `internal_docs/`).

## API boundary

Repo A calls sovereign core only via:

```python
import archovive_core.api as core
# or
from archovive_os.product_v1._core import core
```

Boundary check fails on direct `pipe`, `audit_pipe`, `golden`, or `archovive_engine` imports in product code.

## Customer install

```bash
pip install archovive-core   # private registry
pip install archovive        # public PyPI

archovive bootstrap
archovive simulate
archovive analyze . --out attest.json --package-dir ./sovereign-kit
```

## What `.gitignore` protects

| Risk | Mitigation |
|------|------------|
| Push `sovereign-kit/`, live `attest.json` | Ignored at repo root |
| Push keys / secrets | `*.pem`, `.env*` |
| Push runtime ledgers | `ledger.jsonl`, `zkap_attestation.json` |

`.gitignore` does **not** protect IP if engine source is published — use the dual-repo split.

## Checklist before public push

- [ ] Only Repo A remote on `origin`
- [ ] `scripts/cleanup_repo_a.sh` → `CLEANUP: PASS`
- [ ] `verify_repo_a_boundary.sh` → `BOUNDARY: PASS`
- [ ] No staged `attest.json`, `BUNDLE_MANIFEST.json`, or `*.pem`
- [ ] `archovive-core` wheel on private index only
