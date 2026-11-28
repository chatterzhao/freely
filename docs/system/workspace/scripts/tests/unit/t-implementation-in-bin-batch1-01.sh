#!/usr/bin/env bash
# Function-level contract: batch-1 bin entries are exec projections.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$UT_PROJECT_ROOT"
for pair in raw-issue-pull:sync issue-sync-bootstrap:sync deploy-skills:skills; do
  name="${pair%%:*}"; domain="${pair##*:}"
  wrapper="$ROOT/bin/$name"; truth="$ROOT/docs/system/workspace/scripts/$domain/$name"
  assert_file "$wrapper" "$name bin projection exists"
  assert_file "$truth" "$name truth exists"
  n=$(wc -l < "$wrapper")
  if [[ "$n" -le 8 ]]; then ut_ok "$name projection <=8 lines"; else ut_bad "$name projection $n lines"; fi
  assert_contains "$(cat "$wrapper")" "exec bash" "$name uses exec"
done
python3 "$ROOT/docs/system/workspace/scripts/tests/test-implementation-in-bin-batch1.py" >/dev/null 2>&1
assert_rc "0" "$?" "full batch-1 AT passes"
ut_report
