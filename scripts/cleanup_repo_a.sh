#!/usr/bin/env bash
# Deterministic Repo A hygiene — idempotent. Run on public repo root (post-split).
set -euo pipefail

ROOT="$(cd "${1:-.}" && pwd)"

# 1. Remove directories that must never appear in Repo A
rm -rf "$ROOT/docs/enterprise" \
       "$ROOT/docs/specs" \
       "$ROOT/docs/spec_generator" \
       "$ROOT/docs/pipe" \
       "$ROOT/docs/runtime" \
       "$ROOT/docs/audit" \
       "$ROOT/docs/ledger" \
       "$ROOT/docs/zkap" \
       "$ROOT/docs/internal" \
       "$ROOT/docs/notes" \
       "$ROOT/docs/ideas" \
       "$ROOT/docs/archive" \
       "$ROOT/docs/diagrams" \
       "$ROOT/docs/images" \
       "$ROOT/docs/api" \
       "$ROOT/docs/product_v1" \
       "$ROOT/docs/public" \
       "$ROOT/docs/pilot" \
       "$ROOT/docs/grc" \
       "$ROOT/archovive_os/tests" \
       "$ROOT/archovive_os/demo" \
       "$ROOT/archovive_os/schemas" \
       "$ROOT/archovive_os/scripts" \
       "$ROOT/archovive_os/golden" \
       "$ROOT/archovive_os/pipe" \
       "$ROOT/archovive_os/runtime_pipe" \
       "$ROOT/archovive_os/audit_pipe" \
       "$ROOT/archovive_os/bridge" \
       "$ROOT/archovive_os/contracts" \
       "$ROOT/archovive_os/enterprise" \
       "$ROOT/archovive_os/engine" \
       "$ROOT/archovive_os/tools" \
       "$ROOT/archovive_os/observability" \
       "$ROOT/archovive_os/runtime" \
       "$ROOT/archovive_os/analysis_worlds" \
       "$ROOT/repo_split" \
       "$ROOT/archovive_engine" \
       "$ROOT/archovive_core" \
       "$ROOT/gov"

# 2. Old GRC versions at docs root
find "$ROOT/docs" -maxdepth 1 -type f -name "grc_mapping_v1*" -delete 2>/dev/null || true
find "$ROOT/docs" -maxdepth 1 -type f -name "grc_mapping_v2*" -delete 2>/dev/null || true

# 3. Legacy readmes at docs root
find "$ROOT/docs" -maxdepth 1 -type f -name "README_*" -delete 2>/dev/null || true

# 4. Engine-leak filenames at docs root
find "$ROOT/docs" -maxdepth 1 -type f \( -name "*engine*" -o -name "*core*" -o -name "*golden*" -o -name "*invariant*" \) ! -name "ARCHOVIVE_*" -delete 2>/dev/null || true

# 5. Stray top-level docs (keep only the five canonical files)
for f in "$ROOT/docs"/*; do
  [[ -e "$f" ]] || continue
  base="$(basename "$f")"
  case "$base" in
    ARCHOVIVE_PRODUCT_OVERVIEW.md|ARCHOVIVE_SOVEREIGN_SPEC_V1.md|ARCHOVIVE_BINARY_SUITE.md|ARCHOVIVE_OPEN_CORE_MODEL.md|RELEASE_NOTES_v1.0.0.md) ;;
    *) rm -rf "$f" ;;
  esac
done

# 6. Non-product CLI binaries
rm -f "$ROOT/archovive_os/cli/main.py" \
      "$ROOT/archovive_os/cli/binary_dispatch.py" \
      "$ROOT/archovive_os/cli/canonical.py" \
      "$ROOT/archovive_os/cli/client.py" \
      "$ROOT/archovive_os/cli/completion.py" 2>/dev/null || true

# 7. Legacy renames (no-op if already applied)
mv "$ROOT/docs/ARCHOVIVE_FULL.md" "$ROOT/docs/ARCHOVIVE_PRODUCT_OVERVIEW.md" 2>/dev/null || true
mv "$ROOT/docs/product_v1/SOVEREIGN_PRODUCT_V1.md" "$ROOT/docs/ARCHOVIVE_SOVEREIGN_SPEC_V1.md" 2>/dev/null || true
mv "$ROOT/docs/product_v1/BINARY_KIT.md" "$ROOT/docs/ARCHOVIVE_BINARY_SUITE.md" 2>/dev/null || true
mv "$ROOT/docs/product_v1/DUAL_REPO_MODEL.md" "$ROOT/docs/ARCHOVIVE_OPEN_CORE_MODEL.md" 2>/dev/null || true
mv "$ROOT/docs/product_v1/RELEASE_v1.0.0.md" "$ROOT/docs/RELEASE_NOTES_v1.0.0.md" 2>/dev/null || true

echo "CLEANUP: PASS"
