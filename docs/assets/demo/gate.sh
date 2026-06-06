#!/usr/bin/env bash
# Record: bash docs/assets/demo/gate.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
export PATH="${ROOT}/dist:${PATH}"
cd "${ROOT}"
pip install -q -e internal/ 2>/dev/null || pip install -q --break-system-packages -e internal/
archovive simulate
