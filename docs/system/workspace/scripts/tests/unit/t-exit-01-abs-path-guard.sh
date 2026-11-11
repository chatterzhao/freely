#!/usr/bin/env bash
# Exit contract: a relative --project is refused instead of being silently
# interpreted against the caller's cwd.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ut_load_runtime
ut_require_function abs_path_or_fail

out="$( ( abs_path_or_fail /tmp/freely-unit-probe ) 2>/dev/null )"
assert_rc 0 "$?" "absolute path is accepted"
assert_eq "/tmp/freely-unit-probe" "$out" "absolute path is echoed unchanged"

( abs_path_or_fail relative/path ) >/dev/null 2>&1
assert_rc 1 "$?" "relative path is refused"

( abs_path_or_fail "" ) >/dev/null 2>&1
assert_rc 1 "$?" "empty path is refused"
ut_report
