#!/usr/bin/env bash
# Function-level contract for actionable Gitee comment errors (#4737).
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"

ROOT="$(git rev-parse --show-toplevel)"
RUNTIME="$ROOT/docs/system/workspace/scripts/runtime/gitee-issue.py"
COMMENT="$ROOT/bin/issue-sync.d/cmd-comment.sh"
FINALIZE="$ROOT/bin/issue-sync.d/cmd-promote-finalize.sh"

[[ -f "$RUNTIME" && -f "$COMMENT" && -f "$FINALIZE" ]] \
  && ut_ok "three contract files exist" || ut_bad "contract file missing"

n=$(grep -c 'issue is CLOSED' "$RUNTIME" || true)
assert_eq "1" "$n" "Gitee 401 translated to closed-issue cause"

n=$(grep -c '_gitee_cli get "\$gitee_id"' "$COMMENT" || true)
assert_eq "1" "$n" "comment path reads platform state first"

n=$(grep -c 'closing comment already synced' "$FINALIZE" || true)
assert_eq "1" "$n" "promote-finalize retry guard present"

ut_report
