#!/usr/bin/env bash
# Function-level contract: read-only views tolerate empty agent_working.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$UT_PROJECT_ROOT"
RUNTIME="$ROOT/docs/system/workspace/scripts/runtime/freely"
assert_file "$RUNTIME" "runtime exists"
n=$(grep -c 'FREELY_READONLY_VIEW' "$RUNTIME" || true)
assert_eq "6" "$n" "readonly marker used by load_config guards and three status views"
n=$(grep -c 'FREELY_READONLY_VIEW=1' "$RUNTIME" || true)
assert_eq "3" "$n" "only read-only status views set the marker (no write command)"
python3 "$ROOT/docs/system/workspace/scripts/tests/test-status-readonly-empty-agent.py" >/dev/null 2>&1
assert_rc "0" "$?" "full read-only AT passes"
ut_report
