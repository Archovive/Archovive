#!/usr/bin/env bash
# Record: asciinema rec -c "bash scripts/demo/gate.sh" gate.cast && agg gate.cast docs/assets/gifs/gate.gif
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
export PATH="${ROOT}/dist:${PATH}"
cd "${ROOT}"
pip install -q -e internal/ 2>/dev/null || pip install -q --break-system-packages -e internal/
archovive simulate
