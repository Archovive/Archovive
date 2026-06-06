#!/usr/bin/env bash
# Enterprise preview — drift matrix (for GIF / docs; requires bundle in production).
set -euo pipefail
cat <<'EOF'
$ archovive diff baseline/ HEAD
Drift matrix (compact)
  structural_drift .... measured
  boundary_crossing ... api→payments.ledger
  drift_score ......... 0.42
Exit Code: 1
EOF
