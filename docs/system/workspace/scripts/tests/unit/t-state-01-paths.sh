#!/usr/bin/env bash
# State layout: every runtime file lives under .freely/ and keeps its name.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ut_load_runtime
for fn in workcell_state_file stop_marker_file session_state_file logs_dir_for_project runtime_events_log_file; do
  ut_require_function "$fn"
done

sb="$(ut_sandbox)"
assert_eq "$sb/.freely/run/workcell-state.env" "$(workcell_state_file "$sb")" "workcell state file under .freely/run"
assert_eq "$sb/.freely/run/stop.requested" "$(stop_marker_file "$sb")" "stop marker shares the run dir"
assert_eq "$sb/.freely/run/session-state.env" "$(session_state_file "$sb")" "session state file shares the run dir"
assert_eq "$sb/.freely/logs" "$(logs_dir_for_project "$sb")" "logs live under .freely/logs"
assert_eq "$sb/.freely/logs/runtime-events.log" "$(runtime_events_log_file "$sb")" "runtime events log path"
assert_eq "$sb/.freely/run" "$(run_dir_for_project "$sb")" "run dir is derived from the state dir"
ut_report
