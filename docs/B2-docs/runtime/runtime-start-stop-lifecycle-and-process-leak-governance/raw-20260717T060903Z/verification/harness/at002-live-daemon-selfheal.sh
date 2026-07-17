#!/bin/bash
# AT-002: 真实 daemon 运行中放置 dead 别名 pid 文件 → self-heal 清 dead 且不伤活 claude bridge
set -u
Q="$(pwd)"
_quiesce() {
  "$Q/bin/freely" stop --project "$Q" >/dev/null 2>&1 || true; sleep 2
  for pat in "daemon-run --project $Q" "ensure-manager --project $Q" "ensure-interruption-dispatch --project $Q" "sse-watchdog.sh --project $Q" "watchdog_sse.py --project $Q" "acp-bridge.py start --project $Q"; do pkill -f "$pat" 2>/dev/null || true; done
  for i in 1 2 3 4 5 6; do pgrep -f "project $Q" | grep -qv "^$$\$" || break; sleep 2; done
  rm -f "$Q/.freely/run/stop.requested"
}
_quiesce "$Q"
H=$(python3 -c "import hashlib,os;print(hashlib.sha256(os.path.abspath('$Q').encode()).hexdigest()[:16])")
rm -f /tmp/freely-acp-$H*
"$Q/bin/freely" daemon start --project "$Q" --task-mode wait >/dev/null 2>&1
# 等 claude bridge 起来
for i in $(seq 1 30); do sleep 1; [ -S /tmp/freely-acp-$H-claude.sock ] && break; done
[ -S /tmp/freely-acp-$H-claude.sock ] || { _quiesce "$Q"; echo "AT-002 FAIL: claude bridge 未起(inconclusive)"; exit 0; }
CB_PID=$(cat /tmp/freely-acp-$H-claude.pid 2>/dev/null)
EV="$Q/.freely/logs/runtime-events.log"; M0=$(wc -l < "$EV" | tr -d ' ')
# 放置 dead 别名文件
echo 99999999 > /tmp/freely-acp-$H-ghosttool.pid
: > /tmp/freely-acp-$H-ghosttool.sock
"$Q/bin/freely" live-status --project "$Q" >/dev/null 2>&1   # 触发 self-heal
sleep 3
DEAD_LEFT=$(ls /tmp/freely-acp-$H-ghosttool.* 2>/dev/null | wc -l | tr -d ' ')
LIVE_OK=1
[ -S /tmp/freely-acp-$H-claude.sock ] || LIVE_OK=0
[ "$(cat /tmp/freely-acp-$H-claude.pid 2>/dev/null)" = "$CB_PID" ] || LIVE_OK=0
kill -0 "$CB_PID" 2>/dev/null || LIVE_OK=0
RESPAWN=$(sed -n "$((M0+1)),\$p" "$EV" | grep -c "acp_bridge_started" || true)
_quiesce "$Q"; rm -f /tmp/freely-acp-$H-ghosttool.*
echo "observed: dead_left=$DEAD_LEFT live_ok=$LIVE_OK respawns=$RESPAWN"
if [ "$DEAD_LEFT" -eq 0 ] && [ "$LIVE_OK" -eq 1 ] && [ "$RESPAWN" -eq 0 ]; then
  echo "AT-002 PASS: 清死不伤活且无重生"
else
  echo "AT-002 FAIL: dead_left=$DEAD_LEFT live_ok=$LIVE_OK respawns=$RESPAWN"
fi
