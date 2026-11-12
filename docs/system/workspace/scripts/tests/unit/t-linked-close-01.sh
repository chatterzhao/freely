#!/usr/bin/env bash
# Function-level unit test (Step 2.5): issue-sync close must dispatch on kind so
# a kind=linked I-* document reaches close-linked instead of the strict RAW
# validator that always rejected it.
set -uo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/harness.sh"
ROOT="$(git rev-parse --show-toplevel)"
CLOSE_SH="$ROOT/bin/issue-sync.d/cmd-close.sh"
EFFECTS="$ROOT/docs/system/workspace/scripts/lifecycle/raw_lifecycle_effects.py"

grep -q '_effect_kind' "$CLOSE_SH" && ut_ok "cmd-close reads the document kind" || ut_bad "cmd-close does not branch on kind"
grep -q '"linked"' "$CLOSE_SH" && ut_ok "cmd-close compares against linked" || ut_bad "cmd-close never mentions linked"
grep -q 'close-linked' "$CLOSE_SH" && ut_ok "cmd-close calls close-linked" || ut_bad "cmd-close never calls close-linked"
grep -q 'def close_linked' "$EFFECTS" && ut_ok "close_linked exists" || ut_bad "close_linked missing"
grep -q 'command == "close-linked"' "$EFFECTS" && ut_ok "close-linked is dispatched" || ut_bad "close-linked not dispatched"

tmp="$(mktemp -d "${TMPDIR:-/tmp}/t-linked-close.XXXXXX")"
trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/docs/system/workspace/scripts/sync"
printf 'import sys, json\nprint(json.dumps({"github": {"status": "closed"}}))\nsys.exit(0)\n' \
  > "$tmp/docs/system/workspace/scripts/sync/platform-adapter.py"
cat > "$tmp/raw.md" <<'DOC'
---
schema_version: '1'
local_id: raw-20261112T000000Z
kind: raw
phase_state: absorbed
absorbed_into: I-20261112T000000Z-A
platform_ids:
  github:
    issue_id: '9002'
platform_state: closed
---

# raw
DOC
PYTHONPATH="$ROOT/docs/system/workspace/scripts/lifecycle" python3 "$EFFECTS" close-linked "$tmp/raw.md" "$tmp" >/dev/null 2>&1 \
  && ut_bad "close-linked accepted a kind: raw document" \
  || ut_ok "close-linked refuses kind: raw"

ut_report
