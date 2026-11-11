#!/usr/bin/env bash
# State machine: each runtime role owns exactly one pid file inside .freely/run,
# and an unknown role is an error instead of a shared/empty path.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ut_load_runtime
ut_require_function runtime_pid_file_for_role

sb="$(ut_sandbox)"
assert_eq "$sb/.freely/run/supervisor.pid" "$(runtime_pid_file_for_role "$sb" supervisor)" "supervisor pid file"
assert_eq "$sb/.freely/run/ai.pid" "$(runtime_pid_file_for_role "$sb" ai)" "ai pid file"

( runtime_pid_file_for_role "$sb" not_a_role ) >/dev/null 2>&1
assert_rc 1 "$?" "unknown role is rejected"

ut_report
