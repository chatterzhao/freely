#!/usr/bin/env bash
# Exit contract: project resolution fails closed (rc 1) for a missing dir, a
# relative path, and a directory that was never initialized by `freely init`.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ut_load_runtime
ut_require_function resolve_project_or_fail

sb="$(ut_sandbox)"

( resolve_project_or_fail "$sb/missing" ) >/dev/null 2>&1
assert_rc 1 "$?" "missing project dir is refused"

( resolve_project_or_fail relative/dir ) >/dev/null 2>&1
assert_rc 1 "$?" "relative project path is refused"

mkdir -p "$sb/uninitialized"
( resolve_project_or_fail "$sb/uninitialized" ) >/dev/null 2>&1
assert_rc 1 "$?" "uninitialized project is refused"

mkdir -p "$sb/project/.freely"
: >"$sb/project/.freely/config.toml"
out="$( resolve_project_or_fail "$sb/project" 2>/dev/null )"
assert_rc 0 "$?" "initialized project resolves"
assert_eq "$sb/project" "$out" "resolved path is the project root"
ut_report
