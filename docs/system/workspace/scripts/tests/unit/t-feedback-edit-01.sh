#!/usr/bin/env bash
# Function-level contract: cmd_feedback edit must discover platform ids by raw
# key when the local issue.md is absent (raw-20261125T100958Z / #4704).
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
RUNTIME="$ROOT/docs/system/workspace/scripts/runtime/freely"

body="$(awk '/^cmd_feedback\(\)/{flag=1} flag{print} flag && /^\}/{exit}' "$RUNTIME")"
[[ -n "$body" ]] && ut_ok "cmd_feedback() extracted" || ut_bad "cmd_feedback() extraction failed"

# edit branch only
edit="$(awk '/if \[\[ "\$_subcmd" == "edit" \]\]/{flag=1} flag{print} flag && /^  fi$/{exit}' <<<"$body")"
grep -qF 'platform-adapter.py" search "$raw_key"' <<<"$edit" \
  && ut_ok "edit discovers ids via adapter search" \
  || ut_bad "edit lacks adapter search discovery"

grep -qF 'mktemp' <<<"$edit" \
  && ut_ok "discovery uses temp frontmatter (no local doc created)" \
  || ut_bad "discovery does not use temp file"

grep -qF 'no platform replica found' <<<"$edit" \
  && ut_ok "empty discovery fail-closed" \
  || ut_bad "empty discovery not fail-closed"

# runtime size budget unchanged
lines=$(wc -l < "$RUNTIME"); budget=$(cat "$ROOT/docs/system/workspace/scripts/runtime/.size-budget")
[[ "$lines" -le "$budget" ]] && ut_ok "runtime size within budget ($lines/$budget)" || ut_bad "runtime over budget ($lines/$budget)"
