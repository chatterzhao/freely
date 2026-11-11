#!/usr/bin/env bash
# Observability contract (#4281): every runtime event carries a severity and a
# trace_id, so an operator can filter one run without grepping event names.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ut_load_runtime
ut_require_function append_runtime_event
ut_require_function runtime_events_log_file

sb="$(ut_sandbox)"
append_runtime_event "$sb" probe_failed detail=boom
append_runtime_event "$sb" probe_warn
append_runtime_event "$sb" probe_started
FREELY_TRACE_ID=trace-abc123 append_runtime_event "$sb" probe_tagged

log="$(runtime_events_log_file "$sb")"
assert_file "$log" "runtime events log is created on demand"

line1="$(sed -n '1p' "$log")"
line2="$(sed -n '2p' "$log")"
line3="$(sed -n '3p' "$log")"
line4="$(sed -n '4p' "$log")"

assert_contains "$line1" "event=probe_failed" "event name is recorded"
assert_contains "$line1" "severity=error" "failure events are severity=error"
assert_contains "$line2" "severity=warn" "warning events are severity=warn"
assert_contains "$line3" "severity=info" "ordinary events are severity=info"
assert_contains "$line1" "trace_id=" "every line carries a trace_id"
assert_contains "$line4" "trace_id=trace-abc123" "FREELY_TRACE_ID overrides the trace id"
assert_contains "$line1" "detail=boom" "caller key/value pairs survive"
ut_report
