#!/usr/bin/env bash
# Function-level contract for packaged comment deletion (#4740).
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"

ROOT="$(git rev-parse --show-toplevel)"
ADAPTER="$ROOT/docs/system/workspace/scripts/sync/platform-adapter.py"
GITEE="$ROOT/docs/system/workspace/scripts/runtime/gitee-issue.py"
WRAPPER="$ROOT/bin/issue-sync.d/cmd-comment-delete.sh"

[[ -f "$ADAPTER" && -f "$GITEE" && -f "$WRAPPER" ]] \
  && ut_ok "comment-delete contract files exist" || ut_bad "contract file missing"

n=$(grep -c 'def delete_comment(self, issue_number, comment_id)' "$ADAPTER" || true)
assert_eq "2" "$n" "both platform handlers own comment deletion"

n=$(grep -c 'def delete_comment(local_id: str, platform: str, comment_id: str)' "$ADAPTER" || true)
assert_eq "1" "$n" "adapter validates mapping before delete"

n=$(grep -c 'delete-comment' "$GITEE" || true)
[[ "$n" -ge 2 ]] && ut_ok "Gitee CLI exposes delete-comment" || ut_bad "Gitee CLI missing delete-comment"

ut_report
