#!/usr/bin/env bash
# Function-level unit test (Step 2.5): wt-close branch resolution must never
# double-write the count and must resolve test-pre-merge-only leftovers.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
WT_CLOSE="$ROOT/docs/system/workspace/scripts/worktree/wt-close"
KEY=20261112T131130Z

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
  && ut_ok "test-pre-merge-only leftover is resolvable" \
  || ut_bad "test-pre-merge fallback missing"

tmp="$(mktemp -d "${TMPDIR:-/tmp}/t-wt-count.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT
git init -q "$tmp/repo"
git -C "$tmp/repo" -c user.name=ut -c user.email=ut@local commit --allow-empty -q -m init
git -C "$tmp/repo" branch "test-pre-merge-$KEY-probe"
{
  printf 'set -uo pipefail\n'
  printf '%s\n' "$fn"
  printf "_resolve_branch_from_raw_key '%s'\n" "$KEY"
} > "$tmp/probe.sh"
got="$(cd "$tmp/repo" && bash "$tmp/probe.sh" 2>"$tmp/err")"
rc=$?
if [[ $rc -eq 0 && "$got" == "test-pre-merge-$KEY-probe" ]]; then
  ut_ok "resolver returns the test-pre-merge branch without a syntax error"
else
  ut_bad "resolver failed on a test-pre-merge-only repo (rc=$rc got=$got err=$(cat "$tmp/err"))"
fi

ut_report
