#!/usr/bin/env bash
# Simulated GitHub Actions step + real OSS ci check (exit 2 on demo).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
export PATH="${ROOT}/dist:${PATH}"
cd "${ROOT}"
pip install -q -e internal/ 2>/dev/null || true
echo "▶ Run archovive/ci-gate"
echo "  archovive ci check --repo examples/demo-fintech"
set +e
archovive ci check --repo examples/demo-fintech
code=$?
set -e
echo ""
if [[ "$code" -eq 2 ]]; then
  echo "✗ architecture-gate failed (exit 2) — merge blocked"
  exit 2
fi
exit "$code"
