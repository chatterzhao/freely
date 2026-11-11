#!/usr/bin/env bash
# runtime split, function level (#4160): the helpers that moved into
# runtime/lib/common.sh must behave identically, and the extracted commands must
# keep the exact failure contract they had inline in the monolith.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
RUNTIME="$ROOT/docs/system/workspace/scripts/runtime"
COMMON_LIB="$RUNTIME/lib/common.sh"
MONOLITH="$RUNTIME/freely"

# ── the shared lib is loadable on its own ──
# shellcheck source=/dev/null
source "$COMMON_LIB"
for fn in _log_ts log_info log_warn log_error current_timestamp_utc_for_machine \
          state_dir run_dir_for_project; do
  ut_require_function "$fn"
done

stamp="$(current_timestamp_utc_for_machine)"
case "$stamp" in
  [0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z)
    ut_ok "current_timestamp_utc_for_machine keeps the bare ISO shape" ;;
  *) ut_bad "timestamp shape drifted: $stamp" ;;
esac

assert_eq "/tmp/proj/.freely" "$(state_dir /tmp/proj)" \
  "state_dir falls back to .freely when STATE_DIR_NAME is unset"
assert_eq "/tmp/proj/.freely/run" "$(run_dir_for_project /tmp/proj)" \
  "run_dir_for_project is state_dir + /run"
assert_eq "/tmp/proj/.alt" "$(STATE_DIR_NAME=.alt state_dir /tmp/proj)" \
  "state_dir still honours an explicit STATE_DIR_NAME"

# Warnings go to stderr and never to stdout: a caller parsing stdout must not
# suddenly receive log lines.
out="$(log_error boom 2>/dev/null)"
assert_eq "" "$out" "log_error writes nothing to stdout"
err="$(log_error boom 2>&1 >/dev/null)"
case "$err" in
  *"[ERROR] boom"*) ut_ok "log_error keeps the [ERROR] prefix on stderr" ;;
  *) ut_bad "log_error lost its prefix: $err" ;;
esac

# ── the monolith must not re-grow the helpers it handed over ──
for fn in _log_ts log_info log_warn log_error current_timestamp_utc_for_machine \
          state_dir run_dir_for_project _test_gate_file _test_gate_write; do
  if grep -qE "^${fn}\(\)" "$MONOLITH"; then
    ut_bad "monolith still defines $fn"
  else
    ut_ok "monolith no longer defines $fn"
  fi
done
grep -q 'source "$RUNTIME_COMMON_LIB"' "$MONOLITH" \
  && ut_ok "monolith sources the shared lib" \
  || ut_bad "monolith does not source the shared lib"

# ── extracted entrypoints: same contract as the inline versions ──
GATE="$ROOT/bin/test-gate"
EVBIN="$ROOT/bin/evidence"
assert_eq "2" "$(bash "$GATE" record --status started --worktree /no/such/dir >/dev/null 2>&1; echo $?)" \
  "test-gate record refuses a missing worktree with 2"
assert_eq "2" "$(bash "$GATE" record --worktree /tmp --status bogus >/dev/null 2>&1; echo $?)" \
  "test-gate record refuses an unknown status with 2"
assert_eq "2" "$(bash "$EVBIN" add --file /no/such/file.log >/dev/null 2>&1; echo $?)" \
  "evidence add refuses a missing file with 2"
assert_eq "0" "$(bash "$GATE" --help >/dev/null 2>&1; echo $?)" \
  "test-gate --help exits 0"
assert_eq "1" "$(bash "$GATE" bogus >/dev/null 2>&1; echo $?)" \
  "test-gate rejects an unknown subcommand"
assert_eq "1" "$(bash "$EVBIN" bogus >/dev/null 2>&1; echo $?)" \
  "evidence rejects an unknown subcommand"

# A real test-pre-merge worktree gets its gate file written by the extracted bin.
sandbox="$(ut_sandbox)"
repo="$sandbox/test-pre-merge-unit"
git init -q -b test-pre-merge-unit "$repo"
git -C "$repo" -c user.name=t -c user.email=t@example.com commit -q --allow-empty -m seed
bash "$GATE" record --worktree "$repo" --status completed >/dev/null 2>&1
assert_eq "0" "$?" "test-gate record accepts a test-pre-merge worktree"
grep -q 'TEST_STATUS="completed"' "$repo/.freely/run/test-gate.env" 2>/dev/null \
  && ut_ok "record writes the gate env through run_dir_for_project" \
  || ut_bad "record did not write the gate env"

ut_report
