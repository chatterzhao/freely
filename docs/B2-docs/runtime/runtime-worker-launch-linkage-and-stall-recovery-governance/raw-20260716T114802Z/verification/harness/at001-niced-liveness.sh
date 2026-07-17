#!/usr/bin/env bash
# AT-001: 真实 niced 存活进程（ps 态 SN）必须被 _ai_shows_liveness_acp 判活
set -u
F="$(pwd)/docs/system/workspace/scripts/runtime/freely"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"; kill $NICED 2>/dev/null' EXIT
{
  echo 'file_mtime_epoch() { echo 0; }'                 # S1: debug log 过期(模拟长推理静默)
  echo '_acp_bridge_has_fatal_error() { return 1; }'    # 无 fatal
  echo '_acp_bridge_socket() { echo "/tmp/nonexistent-$$.sock"; }'  # S3 socket 不存在
  echo 'SELF_ROOT="/nonexistent"'                       # S5 无 a2a
  echo 'AGENT_AI_TOOL="claude-apikey-test"'
  awk '/^_ai_shows_liveness_acp\(\)/,/^}/' "$F"
} > "$TMP/h.sh"
nice -n 10 sleep 120 </dev/null >/dev/null 2>&1 &
NICED=$!
sleep 1
STATE=$(ps -o state= -p $NICED | tr -d ' ')
if bash -c "set -u; source '$TMP/h.sh'; _ai_shows_liveness_acp '/tmp/fake-proj' '$NICED' '$TMP/cycle.log' 90" 2>/dev/null; then
  echo "AT-001 PASS: niced 存活进程(state=$STATE)判活"
else
  echo "AT-001 FAIL: niced 存活进程(state=$STATE)被判死(S2 精确匹配击穿)"
fi
