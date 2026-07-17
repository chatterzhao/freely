#!/usr/bin/env bash
# AT-005: usage() --force 描述与 autonomous gate 语义同步（提及自治门禁拒绝判定）
# usage: at005-usage-sync.sh <wtclose_script>
set -uo pipefail
WTC="$1"
out=$(bash "$WTC" --help 2>&1 || true)
if echo "$out" | grep -A2 -- "--force" | grep -q "自治门禁"; then
  echo "AT005_RESULT: PASS"; exit 0
else
  echo "  --force description lacks autonomous-gate wording"
  echo "$out" | grep -A2 -- "--force" | head -4 | sed 's/^/    /'
  echo "AT005_RESULT: FAIL"; exit 1
fi
