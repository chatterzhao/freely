#!/usr/bin/env bash
# Function-level unit test (Step 2.5): wt-close branch resolution never
# double-writes the count and never resolves a test-pre-merge sandbox into a
# close target (that is the companion-only path's job).
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
WT_CLOSE="$ROOT/docs/system/workspace/scripts/worktree/wt-close"
KEY=20261113T084813Z

fn="$(awk '/^_resolve_branch_from_raw_key\(\) \{/{f=1} f{print} f && /^\}$/{exit}' "$WT_CLOSE")"

printf '%s\n' "$fn" | grep -qF 'grep -c . 2>/dev/null || echo 0' \
  && ut_bad "resolver still appends a second zero to the count" \
  || ut_ok "resolver no longer appends a second zero"

printf '%s\n' "$fn" | grep -qF 'grep -c . 2>/dev/null || true' \
  && ut_ok "count capture tolerates grep exit 1" \
  || ut_bad "count capture still fragile"

printf '%s\n' "$fn" | grep -qE '\^\[0-9\]\+\$' \
  && ut_ok "count is validated as a single number" \
  || ut_bad "count has no numeric guard"

printf '%s\n' "$fn" | grep -qF 'test-pre-merge-${raw_key}-*' \
  && ut_bad "resolver still resolves test-pre-merge sandboxes" \
  || ut_ok "resolver does not resolve test-pre-merge sandboxes"

grep -qF '_wt_retire_orphan_test_sandbox() {' "$WT_CLOSE" \
  && ut_ok "companion-only retirement exists" \
  || ut_bad "companion-only retirement missing"

tmp="$(mktemp -d "${TMPDIR:-/tmp}/t-wt-count.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT
git init -q "$tmp/repo"
git -C "$tmp/repo" -c user.name=ut -c user.email=ut@local commit --allow-empty -q -m init
git -C "$tmp/repo" branch "test-pre-merge-$KEY-probe"
run_resolver() {
  {
    printf 'set -uo pipefail\n'
    printf '%s\n' "$fn"
    printf "_resolve_branch_from_raw_key '%s'\n" "$KEY"
  } > "$tmp/probe.sh"
  (cd "$tmp/repo" && bash "$tmp/probe.sh" 2>"$tmp/err")
}

got="$(run_resolver)"; rc=$?
[[ $rc -eq 0 && -z "$got" ]] \
  && ut_ok "sandbox-only repo resolves no close target (no syntax error)" \
  || ut_bad "resolver misbehaved (rc=$rc got=$got err=$(cat "$tmp/err"))"

git -C "$tmp/repo" branch -D "test-pre-merge-$KEY-probe" >/dev/null 2>&1
git -C "$tmp/repo" branch "fix/raw-$KEY-probe"
got="$(run_resolver)"; rc=$?
[[ $rc -eq 0 && "$got" == "fix/raw-$KEY-probe" ]] \
  && ut_ok "single fix branch still resolved" \
  || ut_bad "fix branch resolution regressed (rc=$rc got=$got)"

ut_report
