#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNTIME_DIR="$(cd "$SCRIPT_DIR/../runtime" && pwd)"

find "$RUNTIME_DIR" -type f \( -name '*.sh' -o -name '*.py' \) -exec wc -l {} + | grep -v ' total$' | sort -rn | while read -r count path; do
  echo "$count" "${path#$RUNTIME_DIR/}"
done
