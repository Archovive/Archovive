#!/usr/bin/env bash
# Ensure public product tree contains no engine / gov / benchmark source,
# and no forbidden top-level layout paths (repository standard).
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

FORBIDDEN_TOP=(
  scripts
  tools
  releases
  policy_packs
  archovive
)
for name in "${FORBIDDEN_TOP[@]}"; do
  if [[ -e "${name}" ]]; then
    echo "forbidden top-level path: ${name}/ (see CONTRIBUTING.md#repository-standard)"
    fail=1
  fi
done

for f in pyproject.toml setup.cfg setup.py; do
  if [[ -f "${f}" ]]; then
    echo "forbidden top-level file: ${f} (belongs in internal/)"
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
