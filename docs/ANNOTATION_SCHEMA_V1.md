# Annotation Schema v1 (Brain v2)

**Status:** normative · `annotation_schema_version: annotation_schema_v1`  
**Brain version:** `brain_v2`  
**Vault version:** `vault_v2`

## 1. Purpose

Deterministic semantic annotations over a hypergraph. Advisory only — never in attestation, signature, or `H_verdict` (I2.0–I2.3).

## 2. Layer taxonomy

| Layer | Rule (first match wins) |
|-------|-------------------------|
| `test` | path contains `/test/` or `/tests/` or basename starts with `test_` |
| `external` | path contains `external/` or `node_id` prefix `dep:` |
| `application` | `semantic_layer` = `api` |
| `infrastructure` | `semantic_layer` = `infrastructure` |
| `domain` | default |

Output: `layer_annotation[node_id] → string`

## 3. Pattern taxonomy

Matched on path basename (case-insensitive substring):

`factory`, `adapter`, `facade`, `repository`, `service`, `controller`, `gateway`, `handler`, `provider`, `client`

Output: `pattern_annotation[node_id] → string[]` (sorted unique)

## 4. Anti-pattern taxonomy

| Anti-pattern | Rule |
|--------------|------|
| `god_object` | out-degree > 10 |
| `cyclic_dependency` | node in directed cycle (SCC size > 1) |
| `unstable_interface` | layer `application` and out-degree > 6 |

Output: `anti_pattern_annotation[node_id] → string[]` (sorted unique)

## 5. Architecture signature

```
architecture_signature = stable_hash_v3({
  "architecture_signature_v1": true,
  "layer_distribution": {layer: count},
  "pattern_distribution": {pattern: count},
  "anti_pattern_distribution": {name: count},
  "graph_shape_metrics": {
    "node_count", "edge_count", "component_count", "max_fanout"
  }
})
```

## 6. annotation_hash

```
annotation_hash = stable_hash_v3({
  "annotation_schema_v1": true,
  "layer_annotation": {node_id: layer, ...},  # sorted keys
  "pattern_annotation": {node_id: [patterns], ...},
  "anti_pattern_annotation": {node_id: [anti], ...},
  "architecture_signature": "<hex>"
})
```

## 7. Vault v2 snapshot

```json
{
  "vault_run_id": "<deterministic hex>",
  "graph_hash": "<hex>",
  "annotation_hash": "<hex>",
  "timestamp": "<RFC3339 deterministic from hashes>",
  "delta_to_previous": {
    "added_patterns": [],
    "removed_patterns": [],
    "layer_shifts": [],
    "anti_pattern_changes": []
  },
  "snapshot_hash": "<hex>"
}
```

`vault_run_id = stable_hash_v3({graph_hash, annotation_hash, sequence})`  
`timestamp` MUST NOT use wall-clock in golden/CI (derived from hashes).

## 8. Vault Merkle root

`vault_hash = merkle_root(snapshot_hash[])` over append-only store.

## 9. decision_trace semantic block (v2)

```json
"semantic": {
  "layers": [{"node_id", "layer"}, ...],
  "patterns": [{"node_id", "patterns"}, ...],
  "anti_patterns": [{"node_id", "anti_patterns"}, ...],
  "architecture_signature": "<hex>",
  "annotation_hash": "<hex>",
  "advisory": true,
  "in_verdict": false
}
```

Not copied into attestation material.
