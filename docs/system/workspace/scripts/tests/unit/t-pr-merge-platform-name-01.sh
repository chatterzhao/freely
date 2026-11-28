#!/usr/bin/env bash
# Function-level contract: PR closeout passes configured platform names.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$UT_PROJECT_ROOT"
MERGE="$ROOT/docs/system/workspace/scripts/worktree/pr-merge-guarded"
ADAPTER="$ROOT/docs/system/workspace/scripts/sync/platform-adapter.py"
assert_file "$MERGE" "pr-merge-guarded exists"
assert_file "$ADAPTER" "platform-adapter exists"
n=$(grep -c 'configured-platforms' "$ADAPTER" || true)
assert_eq "1" "$n" "adapter exposes configured-platforms once"
n=$(grep -c 'for platform in \$(git remote' "$MERGE" || true)
assert_eq "0" "$n" "closeout no longer iterates git remotes"
n=$(grep -c 'close-pr \"\$platform\" \"\$source_branch\"' "$MERGE" || true)
assert_eq "1" "$n" "close-pr receives configured platform name"
python3 "$ROOT/docs/system/workspace/scripts/tests/test-pr-merge-platform-name.py" >/dev/null 2>&1
assert_rc "0" "$?" "full AT contract passes"
ut_report
