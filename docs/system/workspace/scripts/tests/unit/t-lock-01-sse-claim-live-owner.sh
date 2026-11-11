#!/usr/bin/env bash
# Lock contract (#4254): one live owner of the SSE watchdog pid file. A second
# claim must fail instead of racing the first writer.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ut_load_runtime
ut_require_function sse_watchdog_claim_pid

sb="$(ut_sandbox)"
pid_file="$sb/sse-watchdog.pid"

sleep 30 &
owner=$!

sse_watchdog_claim_pid "$pid_file" "$owner" ""
assert_rc 0 "$?" "first claim takes the pid file"
assert_eq "$owner" "$(cat "$pid_file")" "pid file records the owner"

sse_watchdog_claim_pid "$pid_file" "$$" ""
assert_rc 1 "$?" "a live owner blocks the second claim"
assert_eq "$owner" "$(cat "$pid_file")" "a refused claim never rewrites the owner"

kill "$owner" 2>/dev/null || true
wait "$owner" 2>/dev/null || true

sse_watchdog_claim_pid "$pid_file" "$$" ""
assert_rc 0 "$?" "a dead owner is taken over"
assert_eq "$$" "$(cat "$pid_file")" "pid file records the new owner"
ut_report
