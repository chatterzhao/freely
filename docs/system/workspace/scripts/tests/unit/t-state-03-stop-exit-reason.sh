#!/usr/bin/env bash
# Exit contract: a stop reason is only preserved for AI exit-contract stops;
# every other cause collapses to operator_stop so dashboards stay meaningful.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ut_load_runtime
ut_require_function runtime_stop_exit_reason

assert_eq "operator_stop" "$(runtime_stop_exit_reason "")" "empty reason becomes operator_stop"
assert_eq "operator_stop" "$(runtime_stop_exit_reason "restart_storm")" "unknown reason becomes operator_stop"
assert_eq "manager_exit_contract_stop_ai" \
  "$(runtime_stop_exit_reason "manager_exit_contract_stop_ai")" "manager exit-contract reason is preserved"
assert_eq "worker_exit_contract_stop_ai" \
  "$(runtime_stop_exit_reason "worker_exit_contract_stop_ai")" "worker exit-contract reason is preserved"
ut_report
