#!/usr/bin/env bash
# Function-level contract for canonical platform identity (#4743).
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"

ROOT="$(git rev-parse --show-toplevel)"
ADAPTER="$ROOT/docs/system/workspace/scripts/sync/platform-adapter.py"
[[ -f "$ADAPTER" ]] && ut_ok "adapter source exists" || ut_bad "adapter missing"

n=$(grep -c 'def is_identity_title' "$ADAPTER" || true)
assert_eq "1" "$n" "single canonical identity helper"

n=$(grep -c 'in:title' "$ADAPTER" || true)
[[ "$n" -ge 1 ]] && ut_ok "platform search queries title" || ut_bad "title query missing"

n=$(grep -c 'needle not in body.lower()' "$ADAPTER" || true)
assert_eq "0" "$n" "body text never defines identity"

ut_report
