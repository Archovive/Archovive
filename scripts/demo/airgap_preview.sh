#!/usr/bin/env bash
# Enterprise preview — isolated mode (requires frozen bundle).
set -euo pipefail
cat <<'EOF'
$ export ARCHOVIVE_ISOLATED=1
$ archovive run
Running in isolated mode (offline bundle)
verify_signature.sh .... OK
ARCHOVIVE GATE — DORA Boundary Crossing
Verdict: POLICY_VIOLATION
Exit Code: 2
EOF
