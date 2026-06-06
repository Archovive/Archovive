#!/usr/bin/env bash
# Enterprise preview — evidence pack export.
set -euo pipefail
cat <<'EOF'
$ archovive audit export --bundle
Writing evidence pack…
  attestation.json
  sbom.json
  file_hashes.json
  compliance_report.json
archovive verify attestation.json .... OK
Evidence pack ready
EOF
