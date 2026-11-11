#!/usr/bin/env bash
# Runner for the core-runtime function tests (#4165).
#
# Every t-*.sh runs in its own bash process: several runtime guards call
# `exit 1` on purpose, and a shared process would turn one guard into a
# truncated run. Each test prints its own `SUMMARY: N ok, M failed`; this
# runner sums them so CI sees one number.
#
#   bash run.sh            # every t-*.sh
#   bash run.sh lock       # only t-lock-*.sh
#   bash run.sh --list     # names only
set -uo pipefail

UT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

filter=""
for arg in "$@"; do
  case "$arg" in
    --list) filter="__list__" ;;
    -h|--help)
      printf '%s\n' "Usage: bash run.sh [prefix|--list]"
      exit 0
      ;;
    *) filter="$arg" ;;
  esac
done

tests=()
for path in "$UT_DIR"/t-*.sh; do
  [[ -f "$path" ]] || continue
  name="$(basename "$path")"
  if [[ "$filter" == "__list__" ]]; then
    printf '%s\n' "$name"
    continue
  fi
  if [[ -n "$filter" && "$name" != t-"$filter"* ]]; then
    continue
  fi
  tests+=("$path")
done

if [[ "$filter" == "__list__" ]]; then
  exit 0
fi

if [[ ${#tests[@]} -eq 0 ]]; then
  echo "[unit] no test files matched" >&2
  exit 2
fi

total_ok=0
total_failed=0
failed_files=""
out="$(mktemp "${TMPDIR:-/tmp}/freely-unit-run.XXXXXX")"
trap 'rm -f "$out"' EXIT

for path in "${tests[@]}"; do
  name="$(basename "$path")"
  printf '=== %s\n' "$name"
  bash "$path" >"$out" 2>&1
  rc=$?
  cat "$out"
  ok=$(awk -F'[: ,]+' '/^SUMMARY:/ {ok=$2} END {print ok+0}' "$out")
  bad=$(awk -F'[: ,]+' '/^SUMMARY:/ {bad=$4} END {print bad+0}' "$out")
  total_ok=$((total_ok + ok))
  total_failed=$((total_failed + bad))
  if [[ "$rc" -ne 0 ]]; then
    failed_files="$failed_files $name"
  fi
done

printf '=== unit: %d file(s), %d ok, %d failed\n' "${#tests[@]}" "$total_ok" "$total_failed"
if [[ -n "$failed_files" ]]; then
  printf 'failing:%s\n' "$failed_files"
  exit 1
fi
[[ "$total_failed" -eq 0 ]] || exit 1
exit 0
