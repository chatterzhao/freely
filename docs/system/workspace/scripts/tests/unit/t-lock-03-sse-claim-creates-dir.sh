#!/usr/bin/env bash
# Lock contract: claiming creates the run dir, so a first boot on a clean
# project does not need the caller to pre-create .freely/run.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ut_load_runtime
ut_require_function sse_watchdog_claim_pid

sb="$(ut_sandbox)"
pid_file="$sb/.freely/run/sse-watchdog.pid"
assert_no_file "$sb/.freely/run" "run dir starts absent"

sse_watchdog_claim_pid "$pid_file" "$$" ""
assert_rc 0 "$?" "claim creates the run dir"
assert_file "$pid_file" "pid file written under the new dir"
ut_report
