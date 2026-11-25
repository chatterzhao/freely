#!/usr/bin/env bash
# Function-level contract: cmd_comment() ACP notification must use the global
# SELF_ROOT, never the unbound PROJECT_ROOT (raw-20261114T111702Z / #4654).
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
RUNTIME="$ROOT/docs/system/workspace/scripts/runtime/freely"

# Global root is defined once at the head of the runtime.
grep -qE '^SELF_ROOT="\$\(cd "\$\(dirname "\$\{BASH_SOURCE\[0\]\}"\)' "$RUNTIME" \
  && ut_ok "SELF_ROOT is defined globally" \
  || ut_bad "SELF_ROOT is not defined globally"

# Extract only cmd_comment() body: from its declaration to the next column-0 brace.
body="$(awk '/^cmd_comment\(\)/{flag=1} flag{print} flag && /^\}/{exit}' "$RUNTIME")"
case "$body" in
  "") ut_bad "cmd_comment() body could not be extracted" ;;
  *)
    ut_ok "cmd_comment() body extracted"
    if grep -qF '${PROJECT_ROOT}' <<<"$body"; then
      ut_bad "cmd_comment() still references unbound PROJECT_ROOT"
    else
      ut_ok "cmd_comment() has no PROJECT_ROOT reference"
    fi
    count="$(grep -oF '${SELF_ROOT}' <<<"$body" | wc -l | tr -d ' ')"
    if [[ "$count" -ge 4 ]]; then
      ut_ok "notification block has $count SELF_ROOT references"
    else
      ut_bad "notification block has only $count SELF_ROOT references (need >=4)"
    fi
    grep -qF 'agent_list_by_raw_key' <<<"$body" \
      && ut_ok "agent_working lookup preserved" \
      || ut_bad "agent_working lookup lost"
    grep -qF 'run-acp-prompt.py' <<<"$body" \
      && ut_ok "ACP notification call preserved" \
      || ut_bad "ACP notification call lost"
    ;;
esac

# Shell syntax must remain valid.
bash -n "$RUNTIME" && ut_ok "runtime passes bash -n" || ut_bad "runtime syntax broken"

# Line budget must not grow.
lines="$(wc -l < "$RUNTIME" | tr -d ' ')"
budget="$(cat "$ROOT/docs/system/workspace/scripts/runtime/.size-budget")"
[[ "$lines" -le "$budget" ]] \
  && ut_ok "runtime lines $lines <= budget $budget" \
  || ut_bad "runtime lines $lines exceed budget $budget"

ut_report
