#!/usr/bin/env bash
# Function-level harness for the core runtime (#4165).
#
# `docs/system/workspace/scripts/runtime/freely` is a 27k-line library that
# `bin/freely` sources; the test corpus only exercised it end to end. This
# harness sources the same file the same way and asserts single-function
# contracts, so a RED can name one function instead of a whole command run.
#
# A test file (t-*.sh) does:
#   source harness.sh
#   ut_load_runtime
#   assert_eq <want> <got> <label>
#   ut_report
#
# ut_report exits 0 iff every assertion passed.

UT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
# unit → tests → scripts → workspace → system → docs → repo
UT_PROJECT_ROOT="${UT_PROJECT_ROOT:-$(cd "$UT_DIR/../../../../../.." && pwd -P)}"
UT_RUNTIME="${UT_RUNTIME:-$UT_PROJECT_ROOT/docs/system/workspace/scripts/runtime/freely}"

UT_PASS=0
UT_FAIL=0
UT_TMPDIRS=""

ut_cleanup() {
  local dir
  for dir in $UT_TMPDIRS; do
    rm -rf "$dir" 2>/dev/null || true
  done
}

ut_sandbox() {
  local dir
  dir="$(mktemp -d "${TMPDIR:-/tmp}/freely-unit.XXXXXX")"
  UT_TMPDIRS="$UT_TMPDIRS $dir"
  printf '%s\n' "$dir"
}

# Source the runtime once per test process. `freely` is a library by design
# (_FREELY_IS_SOURCED, #4153), so loading it must not run main or set -e.
ut_load_runtime() {
  [[ "${_UT_RUNTIME_LOADED:-0}" == "1" ]] && return 0
  if [[ ! -f "$UT_RUNTIME" ]]; then
    printf '  [FATAL] runtime library not found: %s\n' "$UT_RUNTIME" >&2
    exit 2
  fi
  # shellcheck source=/dev/null
  if ! source "$UT_RUNTIME"; then
    printf '  [FATAL] runtime library failed to load: %s\n' "$UT_RUNTIME" >&2
    exit 2
  fi
  _UT_RUNTIME_LOADED=1
}

# Fail the test early when the contract under test no longer exists — a missing
# function must be a RED, never a silently skipped assertion.
ut_require_function() {
  local name="$1"
  if ! declare -F "$name" >/dev/null 2>&1; then
    printf '  [FATAL] required function missing from runtime: %s\n' "$name" >&2
    exit 2
  fi
}

ut_ok() { UT_PASS=$((UT_PASS + 1)); printf '  [ok] %s\n' "$1"; }
ut_bad() { UT_FAIL=$((UT_FAIL + 1)); printf '  [FAIL] %s\n' "$1"; }

assert_eq() {
  local want="$1" got="$2" label="${3:-values differ}"
  if [[ "$want" == "$got" ]]; then
    ut_ok "$label"
  else
    ut_bad "$label (want [$want], got [$got])"
  fi
}

assert_ne() {
  local unwanted="$1" got="$2" label="${3:-value must differ}"
  if [[ "$unwanted" != "$got" ]]; then
    ut_ok "$label"
  else
    ut_bad "$label (both [$got])"
  fi
}

assert_contains() {
  local haystack="$1" needle="$2" label="${3:-contains}"
  case "$haystack" in
    *"$needle"*) ut_ok "$label" ;;
    *) ut_bad "$label (missing [$needle] in [$haystack])" ;;
  esac
}

assert_not_contains() {
  local haystack="$1" needle="$2" label="${3:-does not contain}"
  case "$haystack" in
    *"$needle"*) ut_bad "$label (unexpected [$needle] in [$haystack])" ;;
    *) ut_ok "$label" ;;
  esac
}

assert_file() {
  local path="$1" label="${2:-file exists}"
  if [[ -f "$path" ]]; then
    ut_ok "$label"
  else
    ut_bad "$label (missing $path)"
  fi
}

assert_no_file() {
  local path="$1" label="${2:-file absent}"
  if [[ ! -e "$path" ]]; then
    ut_ok "$label"
  else
    ut_bad "$label (still present $path)"
  fi
}

assert_rc() {
  local want="$1" got="$2" label="${3:-exit code}"
  if [[ "$want" == "$got" ]]; then
    ut_ok "$label"
  else
    ut_bad "$label (want rc=$want, got rc=$got)"
  fi
}

ut_report() {
  printf 'SUMMARY: %d ok, %d failed\n' "$UT_PASS" "$UT_FAIL"
  [[ "$UT_FAIL" -eq 0 ]]
}

trap ut_cleanup EXIT
