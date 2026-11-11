#!/usr/bin/env bash
# Workcell state machine: desired runtime state is read from the state file and
# an unreadable/absent file must read as `unknown`, never as a live guess.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ut_load_runtime
ut_require_function project_desired_runtime_state
ut_require_function workcell_state_file

sb="$(ut_sandbox)"
assert_eq "unknown" "$(project_desired_runtime_state "$sb")" "absent state file reads as unknown"

mkdir -p "$sb/.freely/run"
state="$(workcell_state_file "$sb")"
printf 'DESIRED_RUNTIME_STATE="running"\n' >"$state"
assert_eq "running" "$(project_desired_runtime_state "$sb")" "running is read back"

printf 'DESIRED_RUNTIME_STATE="stopped"\n' >"$state"
assert_eq "stopped" "$(project_desired_runtime_state "$sb")" "stopped is read back"

printf 'LAST_EXIT_REASON="operator_stop"\n' >"$state"
assert_eq "unknown" "$(project_desired_runtime_state "$sb")" "state file without DESIRED_RUNTIME_STATE reads as unknown"
ut_report
