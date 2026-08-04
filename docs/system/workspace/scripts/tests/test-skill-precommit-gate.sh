#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../../.." && pwd -P)"

if ! rg -q 'skills' "$ROOT_DIR/docs/system/workspace/hooks/pre-commit.sh" 2>/dev/null; then
  echo "[FAIL] pre-commit hook has no skills frontmatter validation" >&2
  exit 1
fi

echo "[PASS] pre-commit hook validates skills frontmatter"
