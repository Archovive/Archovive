# Parser strategy (v3 vs v4)

## v3: Regex polyglot IR

Archovive v3 uses **regex-based import extraction** (`polyglot_ir.py`) for:

- Maximum speed on first run
- Zero dependency on Tree-sitter or per-language compiler toolchains
- Deterministic, reproducible graphs in CI

Supported extensions: `.py`, `.go`, `.java`, `.ts`, `.tsx`, `.tf`, `.hcl`.

## v4 roadmap: Tree-sitter

Deep semantics (AST-level edges, call graphs) are planned via **tree-sitter-languages** in v4 only.

## Performance options (v3)

| Env | Effect |
|-----|--------|
| `ARCHOVIVE_CACHE=1` | `.archovive/cache/polyglot_v1/` per-file SHA-256 cache |
| `ARCHOVIVE_POLYGL_PARALLEL=auto` | Process pool when &gt;50 files to parse |
