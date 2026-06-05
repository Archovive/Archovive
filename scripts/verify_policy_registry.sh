#!/usr/bin/env bash
# Ensure open-core policy pack registry uses repo-relative paths.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "${ROOT}"

python3 <<'PY'
import json
from pathlib import Path

reg = json.loads(Path("policy_packs/registry.json").read_text(encoding="utf-8"))
for pack in reg.get("packs", []):
    path = str(pack.get("path", ""))
    if path.startswith("golden/"):
        raise SystemExit(f"forbidden registry path: {path}")
    if not path.startswith("policy_packs/"):
        raise SystemExit(f"expected policy_packs/ prefix: {path}")
print("policy registry OK")
PY
