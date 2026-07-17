#!/usr/bin/env bash
# AT-002: 对活的(argv 伪装)sse-watchdog 装饰进程，valid 判定必须为 valid
set -u
P="$(pwd)"
F="$P/docs/system/workspace/scripts/runtime/freely"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"; kill $DECOY 2>/dev/null' EXIT
{
  echo 'process_inspection_available() { return 0; }'
  echo 'project_paths_equivalent() { [ "$1" = "$2" ]; }'
  awk '/^pid_matches_project\(\)/,/^}/' "$F"
  awk '/^valid_sse_watchdog_pid_for_project\(\)/,/^}/' "$F"
} > "$TMP/h.sh"
PROJ="/tmp/at002-fake-project"
nohup bash -c "exec -a 'runtime/sse-watchdog.sh --project $PROJ --watch' sleep 60" </dev/null >/dev/null 2>&1 &
DECOY=$!
sleep 1
if bash -c "source '$TMP/h.sh'; valid_sse_watchdog_pid_for_project '$PROJ' '$DECOY'"; then
  echo "AT-002 PASS: 活 sse-watchdog 判定 valid"
else
  echo "AT-002 FAIL: 活 sse-watchdog 判定 invalid（参数反转）"
fi
