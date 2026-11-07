#!/usr/bin/env bash
# Bash wrapper around the SINGLE verdict parser (review_verdict.py).
# Source this file, then call: freely_parse_review_verdict <file|"-">
# With "-" the review text is read from stdin (used when the document only
# exists on the remote source branch and must be read via `git show`).
#
# Only "pass" is a passing verdict; callers must fail closed on anything else.
# The `verdict` field name is the sole writer/reader contract (#4150 / #4154).

_FREELY_VERDICT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"

freely_parse_review_verdict() {
  local target="${1:-}"
  local module="$_FREELY_VERDICT_DIR/review_verdict.py"
  if [[ ! -f "$module" ]]; then
    printf 'unknown\n'
    return 1
  fi
  if [[ "$target" == "-" ]]; then
    python3 "$module" --stdin
  elif [[ -n "$target" && -f "$target" ]]; then
    python3 "$module" --file "$target"
  else
    printf 'unknown\n'
  fi
}

freely_review_verdict_is_pass() {
  [[ "$(freely_parse_review_verdict "${1:-}")" == "pass" ]]
}

# Merge-gate decision. Usage:
#   freely_review_verdict_check <file|-> [label]
# Returns 0 ONLY when the document declares the literal verdict `pass`;
# otherwise prints the blocking reason (and the verdict lines it saw) to stderr
# and returns 1. Missing/empty documents are blocked in the same place, so the
# guard cannot distinguish "no review" from "review says no" by accident.
freely_review_verdict_check() {
  local target="${1:-}" label="${2:-review}" text verdict
  if [[ "$target" == "-" ]]; then
    text="$(cat)"
  elif [[ -n "$target" && -f "$target" ]]; then
    text="$(cat "$target")"
  else
    text=""
  fi
  if [[ -z "$text" ]]; then
    printf '[verdict] %s: review document missing or empty -> blocked\n' "$label" >&2
    return 1
  fi
  verdict="$(printf '%s\n' "$text" | freely_parse_review_verdict - 2>/dev/null || printf 'unknown\n')"
  if [[ "$verdict" == "pass" ]]; then
    return 0
  fi
  printf '[verdict] %s: verdict=%s (expected pass) -> blocked\n' "$label" "$verdict" >&2
  printf '%s\n' "$text" \
    | grep -iE '^[[:space:]]*[-*+]?[[:space:]]*verdict[[:space:]]*:' \
    | head -5 | sed 's/^/  /' >&2 || true
  return 1
}
