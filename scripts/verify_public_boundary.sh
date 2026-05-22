#!/usr/bin/env bash
# Ensure public repo contains no engine / gov / benchmark trees.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

FORBIDDEN=(
  archovive_engine
  archovive_os/core
  archovive_os/bridge
  archovive_os/pipe
  gov
  benchmarks
  product_bundle
  polyglot_ir.py
  sbom_evidence.py
  evidence.py
)

fail=0
for pattern in "${FORBIDDEN[@]}"; do
  if find . -path "./.git" -prune -o -name "${pattern}" -print -quit 2>/dev/null | grep -q .; then
    echo "forbidden path present: ${pattern}"
    find . -path "./.git" -prune -o -name "${pattern}" -print 2>/dev/null | head -5
    fail=1
  fi
done

# Legacy v1 tree must be gone
if [[ -d archovive_os/product_v1 ]]; then
  echo "remove legacy archovive_os/product_v1"
  fail=1
fi

if [[ "${fail}" -ne 0 ]]; then
  exit 1
fi
echo "public boundary OK"
