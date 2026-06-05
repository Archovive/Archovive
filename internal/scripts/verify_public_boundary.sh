#!/usr/bin/env bash
# Ensure public product tree contains no engine / gov / benchmark source.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "${ROOT}"

FORBIDDEN=(
  archovive_engine
  archovive_os/core
  archovive_os/bridge
  archovive_os/pipe
  gov
  benchmarks
  polyglot_ir.py
  sbom_evidence.py
  evidence.py
)

fail=0
for pattern in "${FORBIDDEN[@]}"; do
  if find . -path "./.git" -prune -o -path "./internal" -prune -o -name "${pattern}" -print -quit 2>/dev/null | grep -q .; then
    echo "forbidden path present outside internal/: ${pattern}"
    find . -path "./.git" -prune -o -path "./internal" -prune -o -name "${pattern}" -print 2>/dev/null | head -5
    fail=1
  fi
done

if [[ -d archovive_os/product_v1 ]]; then
  echo "remove legacy archovive_os/product_v1 from product tree"
  fail=1
fi

if [[ "${fail}" -ne 0 ]]; then
  exit 1
fi
echo "public boundary OK"
