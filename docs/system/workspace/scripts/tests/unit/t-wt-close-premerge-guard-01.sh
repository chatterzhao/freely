#!/usr/bin/env bash
# Function-level unit test (Step 2.5): the protected-branch guard must keep
# main/develop refused while allowing a disposable test-pre-merge sandbox to be
# retired with BOTH --force and --discard-unmerged.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
WT_CLOSE="$ROOT/docs/system/workspace/scripts/worktree/wt-close"

helper="$(awk '/^_is_protected_branch\(\) \{/{f=1} f{print} f && /^\}$/{exit}' "$WT_CLOSE")"
guard="$(awk '/^# ── Guard: protected branch/{f=1} f{print} f && /^# ── Resolve worktree path/{exit}' "$WT_CLOSE" | sed '$d')"

printf '%s\n' "$guard" | grep -qF 'test-pre-merge-*' \
  && ut_ok "guard has a test-pre-merge exception" \
  || ut_bad "guard has no test-pre-merge exception"

printf '%s\n' "$guard" | grep -qF '$FORCE" == true && "$DISCARD_UNMERGED" == true' \
  && ut_ok "exception requires both flags" \
  || ut_bad "exception does not require both flags"

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

run_case test-pre-merge-20261112T040108Z-probe true true \
  && ut_ok "test-pre-merge passes with both flags" \
  || ut_bad "test-pre-merge still refused with both flags"

run_case test-pre-merge-20261112T040108Z-probe true false \
  && ut_bad "test-pre-merge passed without --discard-unmerged" \
  || ut_ok "test-pre-merge refused without --discard-unmerged"

run_case develop true true \
  && ut_bad "develop was closable" \
  || ut_ok "develop stays protected"

ut_report
