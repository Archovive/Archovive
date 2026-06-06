#!/usr/bin/env bash
# Enterprise preview — compact run output (requires bundle).
set -euo pipefail
cat <<'EOF'
$ archovive run --compact
[1/4] Architecture graph
  boundary_crossings ... 1
[3/4] Policy evaluation
  [FAIL] DORA_2026 :: dora_crossings_max
Verdict: POLICY_VIOLATION
Exit Code: 2
EOF
