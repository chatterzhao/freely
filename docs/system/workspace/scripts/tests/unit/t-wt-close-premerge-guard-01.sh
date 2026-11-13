#!/usr/bin/env bash
# Function-level unit test (Step 2.5): the protected-branch guard stays
# absolute (main/develop/test-pre-merge all refused), while orphan sandboxes
# are retired by the companion-only path.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
WT_CLOSE="$ROOT/docs/system/workspace/scripts/worktree/wt-close"
KEY=20261113T084813Z

helper="$(awk '/^_is_protected_branch\(\) \{/{f=1} f{print} f && /^\}$/{exit}' "$WT_CLOSE")"
guard="$(awk '/^# ── Guard: protected branch/{f=1} f{print} f && /^# ── Resolve worktree path/{exit}' "$WT_CLOSE" | sed '$d')"
companion="$(awk '/^_wt_retire_orphan_test_sandbox\(\) \{/{f=1} f{print} f && /^\}$/{exit}' "$WT_CLOSE")"

printf '%s\n' "$guard" | grep -qF '$FORCE" == true && "$DISCARD_UNMERGED" == true' \
  && ut_bad "guard still has a --force exception" \
  || ut_ok "guard has no --force/--discard-unmerged exception"

printf '%s\n' "$guard" | grep -qF 'is a protected branch, cannot close' \
  && ut_ok "guard still emits the refusal message" \
  || ut_bad "guard refusal message missing"

printf '%s\n' "$companion" | grep -qF 'no platform close / no Phase 7 develop sync' \
  && ut_ok "companion-only path declares zero platform/develop side effects" \
  || ut_bad "companion path missing"

tmp="$(mktemp -d "${TMPDIR:-/tmp}/t-premerge-guard.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT
run_case() {
  local branch="$1" force="$2" discard="$3"
  {
    printf 'set -uo pipefail\n'
    printf '%s\n' "$helper"
    printf "branch='%s'\nFORCE=%s\nDISCARD_UNMERGED=%s\n" "$branch" "$force" "$discard"
    printf '%s\n' "$guard"
    printf 'echo GUARD_PASSED\n'
  } > "$tmp/probe.sh"
  bash "$tmp/probe.sh" >/dev/null 2>&1
}

run_case "test-pre-merge-$KEY-probe" true true \
  && ut_bad "test-pre-merge was closable through the guard" \
  || ut_ok "test-pre-merge refused even with both flags"

run_case develop true true \
  && ut_bad "develop was closable" \
  || ut_ok "develop stays protected"

run_case "fix/raw-$KEY-probe" true true \
  && ut_ok "fix branch unaffected by the guard" \
  || ut_bad "fix branch was refused"

ut_report
