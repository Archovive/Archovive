# Archovive Public Compiler Specification v1

**Status:** normative · `compiler_spec_version: compiler_spec_v1`  
**Compiler version:** `v1`

## 1. Purpose

Enable trustless verification: an auditor recomputes `graph_hash` from source using only the public `archivive-compile` binary — no `archovive_engine`, no private monorepo, no proprietary semantics.

## 2. Invocation

```bash
archovive-compile <repo_path>
```

Stdout: single JSON object (UTF-8, LF, no trailing noise):

```json
{
  "graph_hash": "<hex>",
  "pipeline_identity": {
    "compiler_version": "v1",
    "compiler_spec_hash": "<hex>",
    "compiler_binary_hash": "<hex>"
  }
}
```

## 3. Compiler input

- `repo_path`: directory containing source files. Resolved to absolute path, normalized to POSIX `/` separators.
- Skipped directory names: `.git`, `__pycache__`, `.venv`, `node_modules`, `dist`, `build`, `.gov`
- Supported extensions: `.py`, `.go`, `.java`, `.ts`, `.tsx`, `.tf`, `.hcl`

## 4. IR (polyglot_ir_v1)

Per file:

| Field | Type | Rule |
|-------|------|------|
| `path` | string | Relative to repo root, POSIX |
| `language` | string | From extension map |
| `imports` | string[] | Sorted unique, parser rules below |
| `line_count` | int | `count("\n") + (1 if non-empty else 0)` |

Import parsers (line-anchored regex, same as reference):

- **python:** `^\s*(?:from|import)\s+([\w.]+)`
- **go:** `^\s*import\s+(?:\([\s\S]*?\)|"([^"]+)")`
- **java:** `^\s*import\s+([\w.]+)\s*;`
- **typescript:** `^\s*import\s+.*?from\s+['"]([^'"]+)['"]`
- **terraform:** `^\s*(?:module|resource|data)\s+"([^"]+)"`

IR body hash: `stable_hash_v3(ir_body)` where `ir_body` excludes `ir_hash`.

## 5. Hypergraph schema

### 5.1 Node

| Field | Value |
|-------|-------|
| `node_id` | `file:<path>` or `dep:<import>` |
| `layer` | `code_ast` |
| `attrs.path` | file path or import string |
| `attrs.file` | same as path for file nodes |
| `attrs.entity_type` | `file` or `module` |
| `attrs.language` | IR language |
| `attrs.semantic_layer` | `api` if language ∈ {typescript, go}; else `domain` for files; `infrastructure` for deps |

### 5.2 Edge

| Field | Value |
|-------|-------|
| `src` | `file:<path>` |
| `dst` | `dep:<import>` |
| `kind` | `import` |

Nodes and edges sorted lexicographically by `(node_id)` and `(src, dst, kind)` before hashing.

## 6. graph_hash (compiler_graph_v1)

```
graph_hash = stable_hash_v3({
  "compiler_graph_v1": true,
  "repo_path": canonical_repo_path,
  "ir_hash": <ir_hash from section 4>,
  "nodes": [ { "node_id", "layer", "attrs": {sorted keys} }, ... ],
  "edges": [ { "src", "dst", "kind" }, ... ]
})
```

**Not included:** wall-clock time, randomness, OS-specific absolute paths in `repo_path` (use repo-relative fingerprint: `stable_hash_v3({"repo": posix_relative_if_under_cwd else basename})` — reference uses **basename only** for golden-repo portability: `repo_id = Path(repo_path).name`).

> **Normative for golden repos:** `repo_path` in hash preimage is `Path(repo_path).resolve().name` (final directory name only).

## 7. stable_hash_v3

```python
canonical = json.dumps({"v": 3, "payload": payload}, sort_keys=True, separators=(",", ":"), default=str)
graph_hash = sha256(canonical).hexdigest()
```

Implementations MUST use identical JSON canonicalization.

## 8. Determinism constraints

- No wall-clock time in compiler output (except transparency log, separate)
- No randomness
- No thread races (single-threaded compile)
- Sorted iteration over files, nodes, edges, map keys

## 9. Transparency log entry

```json
{
  "attestation_hash": "<hex>",
  "graph_hash": "<hex>",
  "pipeline_identity": { "compiler_version": "v1", "compiler_spec_hash": "<hex>", "compiler_binary_hash": "<hex>" },
  "timestamp": "<RFC3339 UTC>",
  "entry_hash": "<hex>",
  "merkle_root": "<hex>"
}
```

`entry_hash = stable_hash_v3({attestation_hash, graph_hash, pipeline_identity, timestamp})`  
Merkle root over ordered `entry_hash` list (binary tree, pad with duplicate last if odd).

## 10. Verify algorithm (standalone_verify v2)

1. Load attestation JSON  
2. Verify Ed25519/ECDSA signature on preimage (see exhibit `signature_preimage`)  
3. Extract `repo` path from attestation  
4. Run `archovive-compile <repo>`  
5. Compare `graph_hash` to `attestation.compiler_graph_hash` or `attestation.graph_hash` when `compiler_graph_hash` absent (legacy)  
6. Verify transparency log contains `attestation_hash` with matching `graph_hash` and current `merkle_root` in trust anchor  
7. Emit PASS or FAIL  

## 11. Versioning

| Field | v1 value |
|-------|----------|
| `compiler_spec_version` | `compiler_spec_v1` |
| `compiler_version` | `v1` |
| `ir_version` | `polyglot_ir_v1` |

Spec changes require new `compiler_spec_hash` and pipeline identity bump.
