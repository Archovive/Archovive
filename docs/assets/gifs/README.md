# Demo GIFs

Terminal animations for the public README and docs. **NovaPay** uses the same gate as `gate.gif` — no separate file (avoid duplication).

**Last regenerated:** 2026-06-06 (commit `566e906`) — update this line when you run `make gifs`.

GIFs marked **Enterprise bundle** are previews of bundle commands (this repo routes to the bundle; it does not ship the full engine).

## Files

| File | OSS? | Record command |
|------|------|----------------|
| `gate.gif` | Yes | `bash docs/assets/demo/gate.sh` |
| `ci.gif` | Yes | `bash docs/assets/demo/ci_gate.sh` |
| `drift.gif` | Enterprise bundle | `bash docs/assets/demo/drift_preview.sh` |
| `airgap.gif` | Enterprise bundle | `bash docs/assets/demo/airgap_preview.sh` |
| `evidence.gif` | Enterprise bundle | `bash docs/assets/demo/evidence_preview.sh` |
| `graph.gif` | Enterprise bundle | `bash docs/assets/demo/graph_preview.sh` |

## Regenerate (preferred: VHS)

Requires **vhs** + **ffmpeg**:

```bash
# install once
go install github.com/charmbracelet/vhs@latest
# ffmpeg: https://ffmpeg.org

bash docs/assets/demo/build_gifs.sh
```

Or from the repo root: `make gifs`

VHS tape files: `docs/assets/demo/tapes/*.tape`

## Fallback (no VHS / ffmpeg)

```bash
python3 docs/assets/demo/build_gifs.py
```

Auto-cropped Pillow GIFs — smaller canvas, no terminal chrome. Use VHS when possible for real CLI recordings.

## Record with asciinema (optional)

```bash
pip install asciinema agg
asciinema rec -c "bash docs/assets/demo/gate.sh" gate.cast
agg gate.cast docs/assets/gifs/gate.gif
```
