#!/usr/bin/env bash
# Lock contract: a pid left behind by a dead process must not block a restart.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ut_load_runtime
ut_require_function sse_watchdog_claim_pid

sb="$(ut_sandbox)"
pid_file="$sb/sse-watchdog.pid"
printf '999999\n' >"$pid_file"

sse_watchdog_claim_pid "$pid_file" "$$" ""
assert_rc 0 "$?" "a stale pid is taken over"
assert_eq "$$" "$(cat "$pid_file")" "stale pid is replaced"
ut_report
