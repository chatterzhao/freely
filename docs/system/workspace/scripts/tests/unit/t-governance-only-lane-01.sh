#!/usr/bin/env bash
# Function-level contract: governance-only lane is config-driven and bounded.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$UT_PROJECT_ROOT"
GATE="$ROOT/docs/system/workspace/scripts/quality/governance-merge-gate"
assert_file "$GATE" "governance-merge-gate exists"
n=$(grep -c 'L2: hardcoded defaults' "$GATE" || true)
assert_eq "0" "$n" "no second hardcoded allowlist"
n=$(grep -c 'FREELY_SKIP_IBM_GATE' "$GATE" || true)
assert_ne "0" "$n" "skip command documented in gate"
python3 "$ROOT/docs/system/workspace/scripts/tests/test-governance-only-lane.py" >/dev/null 2>&1
assert_rc "0" "$?" "full lane AT passes"
ut_report
