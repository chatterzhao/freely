#!/bin/bash
# AT-001: 沙箱 — 一死一活两组 pid 文件, self-heal 后死组全清、活组完好
set -u
F="$(pwd)/docs/system/workspace/scripts/runtime/freely"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"; kill $LIVE 2>/dev/null' EXIT
H="testhash00000000"
sleep 300 & LIVE=$!
# 活组: faketool  死组: deadtool
for ext in pid sock pid.bin pid.tool; do : > "$TMP/freely-acp-$H-faketool.$ext"; : > "$TMP/freely-acp-$H-deadtool.$ext"; done
echo $LIVE > "$TMP/freely-acp-$H-faketool.pid"
echo 99999999 > "$TMP/freely-acp-$H-deadtool.pid"
{
  echo 'append_runtime_event() { :; }'
  echo 'pid_hint_from_file_without_process_inspection() { :; }'
  echo "_acp_bridge_short_hash() { echo $H; }"
  echo "FREELY_ACP_TMPDIR=$TMP"
  awk '/^_clear_stale_acp_bridge_pid_file_if_invalid\(\)/,/^}/' "$F"
} > "$TMP/h.sh"
if ! grep -q "_clear_stale_acp_bridge_pid_file_if_invalid" "$TMP/h.sh"; then
  echo "AT-001 FAIL: per-tool self-heal 函数不存在"; exit 0
fi
bash -c "source '$TMP/h.sh'; for pf in '$TMP'/freely-acp-$H-*.pid; do _clear_stale_acp_bridge_pid_file_if_invalid 'dummy' \"\$pf\"; done" 2>/dev/null
DEAD_LEFT=$(ls "$TMP"/freely-acp-$H-deadtool.* 2>/dev/null | wc -l | tr -d ' ')
LIVE_LEFT=$(ls "$TMP"/freely-acp-$H-faketool.* 2>/dev/null | wc -l | tr -d ' ')
echo "observed: dead_left=$DEAD_LEFT live_left=$LIVE_LEFT"
if [ "$DEAD_LEFT" -eq 0 ] && [ "$LIVE_LEFT" -eq 4 ]; then echo "AT-001 PASS: 清死不伤活"; else echo "AT-001 FAIL: dead=$DEAD_LEFT live=$LIVE_LEFT"; fi
