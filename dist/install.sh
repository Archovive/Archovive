#!/usr/bin/env bash
# OSS quickstart — simulate demo in 30 seconds (no enterprise bundle required).
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${REPO_ROOT}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "archovive: Python 3.11+ required" >&2
  exit 1
fi

PY="${PYTHON:-python3}"
if ! "${PY}" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3, 11) else 1)'; then
  echo "archovive: Python 3.11+ required" >&2
  exit 1
fi

echo "==> Archovive OSS quickstart"
"${PY}" -m pip install -q -e "${REPO_ROOT}/internal" 2>/dev/null || \
  "${PY}" -m pip install -q --break-system-packages -e "${REPO_ROOT}/internal"

export PATH="${REPO_ROOT}/dist:${PATH}"
echo "==> Try: archovive simulate"
archovive simulate
echo ""
echo "Next: docs/README.md (pick your path)"
