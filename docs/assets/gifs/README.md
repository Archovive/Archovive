# Demo GIFs

Terminal animations for the public README and docs. **NovaPay** uses the same gate as `gate.gif` — no separate file (avoid duplication).

GIFs marked **Enterprise bundle** are stylized previews of bundle commands (this repo routes to the bundle; it does not ship the full engine).

## Files

| File | OSS? | Record command |
|------|------|----------------|
| `gate.gif` | Yes | `bash scripts/demo/gate.sh` |
| `ci.gif` | Yes | `bash scripts/demo/ci_gate.sh` |
| `drift.gif` | Enterprise bundle | `bash scripts/demo/drift_preview.sh` |
| `airgap.gif` | Enterprise bundle | `bash scripts/demo/airgap_preview.sh` |
| `evidence.gif` | Enterprise bundle | `bash scripts/demo/evidence_preview.sh` |
| `graph.gif` | Enterprise bundle | `bash scripts/demo/graph_preview.sh` |

## Regenerate (no asciinema required)

```bash
python3 scripts/demo/build_gifs.py
```

## Record from real terminal (optional)

```bash
pip install asciinema agg  # or use vhs
asciinema rec -c "bash scripts/demo/gate.sh" gate.cast
agg gate.cast docs/assets/gifs/gate.gif
```
