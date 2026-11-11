#!/usr/bin/env bash
# Lock contract: one triage per intake. The second acquire fails while held and
# succeeds again after release, so a crashed triage cannot wedge the intake.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ut_load_runtime
ut_require_function acquire_interruption_triage_lock_for_intake
ut_require_function release_interruption_triage_lock_for_intake
ut_require_function interruption_triage_lock_dir_for_intake

sb="$(ut_sandbox)"
intake="intake-20260101T000000Z"

acquire_interruption_triage_lock_for_intake "$sb" "$intake"
assert_rc 0 "$?" "first triage acquires the lock"
assert_file "$(interruption_triage_lock_dir_for_intake "$sb" "$intake")/state.env" "lock state records the owner"

acquire_interruption_triage_lock_for_intake "$sb" "$intake"
assert_rc 1 "$?" "second triage is refused while held"

release_interruption_triage_lock_for_intake "$sb" "$intake"
assert_rc 0 "$?" "release succeeds"
assert_no_file "$(interruption_triage_lock_dir_for_intake "$sb" "$intake")" "lock dir removed on release"

acquire_interruption_triage_lock_for_intake "$sb" "$intake"
assert_rc 0 "$?" "intake can be triaged again after release"
ut_report
