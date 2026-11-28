#!/usr/bin/env bash
# Function-level contract: documented command names resolve to dispatcher/bin.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"

ROOT="$UT_PROJECT_ROOT"
CHECKER="$ROOT/docs/system/workspace/scripts/quality/command_name_contract.py"

assert_file "$CHECKER" "command name contract checker exists"

python3 "$CHECKER" --self-test >/dev/null 2>&1
assert_rc "0" "$?" "self-test accepts valid command and rejects synthetic unknown one"

python3 "$CHECKER" --root "$ROOT" >/dev/null 2>&1
assert_rc "0" "$?" "live repository has no unresolved command promise"

# Synthetic negative: a documented command absent from dispatcher and bin must
# fail closed (not silently pass).
sandbox="$(ut_sandbox)"
mkdir -p "$sandbox/bin" "$sandbox/docs/system/workspace/scripts/runtime" "$sandbox/docs/system/workspace"
printf '%s\n' 'main() {' '  case "$cmd" in' '    status) cmd_status "$@" ;;' '  esac' '}' \
  > "$sandbox/docs/system/workspace/scripts/runtime/freely"
printf '%s\n' 'see `freely bogus-command` for details' \
  > "$sandbox/docs/system/workspace/commands.md"
python3 "$CHECKER" --root "$sandbox" >/dev/null 2>&1
assert_rc "1" "$?" "synthetic undocumented command is rejected (fail-closed)"

ut_report
