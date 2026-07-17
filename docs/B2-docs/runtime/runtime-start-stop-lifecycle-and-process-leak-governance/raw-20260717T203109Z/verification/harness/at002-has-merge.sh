#!/usr/bin/env bash
# AT-002: _has_merge 对已合并 raw key 稳定判 true（foreign+merged → allowing sweep），无 SIGPIPE×pipefail 竞态
# usage: at002-has-merge.sh <wtclose_script> <dev_worktree_dir> [rounds]
set -uo pipefail
WTC="$1"; DW="$2"; ROUNDS="${3:-5}"
MERGED_KEY=20260717T004620Z
T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
cd "$DW"
pass=0
for i in $(seq 1 "$ROUNDS"); do
  env -u FREELY_AGENT_RAW_KEY PROJECT_ROOT="$DW" bash "$WTC" --raw-key "$MERGED_KEY" --dry-run 2>"$T/r$i.log" >/dev/null
  grep -q "allowing sweep" "$T/r$i.log" && pass=$((pass+1))
done
echo "  rounds passed: $pass/$ROUNDS"
if [[ "$pass" -eq "$ROUNDS" ]]; then echo "AT002_RESULT: PASS"; exit 0; else echo "AT002_RESULT: FAIL"; sed -n '1,3p' "$T/r1.log" | sed 's/^/    /'; exit 1; fi
