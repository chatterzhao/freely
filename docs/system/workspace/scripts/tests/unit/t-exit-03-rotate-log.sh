#!/usr/bin/env bash
# Exit contract: rotation is size-triggered and keeps a bounded ring. A log
# below the threshold must be left alone (no gratuitous inode churn).
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ut_load_runtime
ut_require_function _rotate_log

sb="$(ut_sandbox)"
log="$sb/cycle.log"

printf '%s' "small" >"$log"
_rotate_log "$log" 100 2
assert_eq "small" "$(cat "$log")" "below-threshold log is untouched"
assert_no_file "$log.0" "no rotation happened below the threshold"

# 400+ bytes > threshold 100
python3 -c 'print("x" * 400)' >"$log"
_rotate_log "$log" 100 2
assert_eq "" "$(cat "$log")" "active log is truncated after rotation"
assert_file "$log.0" "rotated file .0 exists"
assert_eq "400" "$(tr -d '\n' <"$log.0" | wc -c | tr -d ' ')" "rotated file keeps the previous bytes"

python3 -c 'print("y" * 400)' >"$log"
_rotate_log "$log" 100 2
assert_file "$log.1" "second rotation shifts .0 to .1"
assert_contains "$(head -c 1 "$log.0")" "y" "newest rotated file is .0"
ut_report
