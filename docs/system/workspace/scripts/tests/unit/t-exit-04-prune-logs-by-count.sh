#!/usr/bin/env bash
# Retention contract (#4281): per-run logs (cycle-*/crash-*) are bounded by
# COUNT, because _rotate_log only bounds a single growing file. Newest win.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ut_load_runtime
ut_require_function _prune_logs_by_count

sb="$(ut_sandbox)"
logs="$sb/logs"
mkdir -p "$logs"
i=1
while [[ "$i" -le 5 ]]; do
  printf 'cycle %s\n' "$i" >"$logs/cycle-$i.log"
  # Distinct mtimes: `ls -1t` needs a total order to pick the newest N.
  touch -t "20260101000${i}.00" "$logs/cycle-$i.log"
  i=$((i + 1))
done

_prune_logs_by_count "$logs" 'cycle-*.log' 2
assert_rc 0 "$?" "prune succeeds"
assert_eq "2" "$(ls -1 "$logs" | wc -l | tr -d ' ')" "only two cycle logs survive"
assert_file "$logs/cycle-5.log" "newest log is kept"
assert_file "$logs/cycle-4.log" "second newest is kept"
assert_no_file "$logs/cycle-1.log" "oldest log is pruned"

# A keep count of 0 or a bogus value must not delete anything unexpected: the
# guard falls back to the default instead of treating it as "remove all".
printf 'cycle 9\n' >"$logs/crash-9.log"
_prune_logs_by_count "$logs" 'cycle-*.log' not-a-number
assert_file "$logs/crash-9.log" "non-matching files are untouched"
ut_report
