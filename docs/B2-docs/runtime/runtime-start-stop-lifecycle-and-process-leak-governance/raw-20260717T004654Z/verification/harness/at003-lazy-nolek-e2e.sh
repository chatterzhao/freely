#!/usr/bin/env bash
# AT-003: wait 模式 100s——仅 manager bridge 启动(事件≤1)、存活 bridge≤1、opencode/cline=0
set -u
P="$(pwd)"
_quiesce() {
  local proj="$1"
  "$proj/bin/freely" stop --project "$proj" >/dev/null 2>&1 || true
  sleep 2
  for pat in "daemon-run --project $proj" "ensure-manager --project $proj" "ensure-interruption-dispatch --project $proj" "sse-watchdog.sh --project $proj" "watchdog_sse.py --project $proj" "acp-bridge.py start --project $proj"; do
    pkill -f "$pat" 2>/dev/null || true
  done
  local hash; hash=$(python3 -c "import hashlib,os;print(hashlib.sha256(os.path.abspath('$proj').encode()).hexdigest()[:16])" 2>/dev/null)
  [ -n "$hash" ] && rm -f /tmp/freely-acp-${hash}-* 2>/dev/null
  for i in 1 2 3 4 5 6 7 8; do pgrep -f "project $proj" | grep -qv "^$$\$" || break; sleep 2; done
  rm -f "$proj/.freely/run/stop.requested"
}
_quiesce "$P"
EV="$P/.freely/logs/runtime-events.log"; mkdir -p "$P/.freely/logs"; touch "$EV"
M0=$(wc -l < "$EV" | tr -d ' ')
"$P/bin/freely" daemon start --project "$P" --task-mode wait >/dev/null 2>&1
sleep 100
NEW="$(sed -n "$((M0+1)),\$p" "$EV")"
SPAWNS=$(printf '%s\n' "$NEW" | grep -c "event=acp_bridge_started" || true)
BRIDGES=$(pgrep -f "acp-bridge.py start --project $P" | wc -l | tr -d ' ')
OC=$(pgrep -f "acp-bridge.py start --project $P --base-tool opencode" | wc -l | tr -d ' ')
CL=$(pgrep -f "acp-bridge.py start --project $P --base-tool cline" | wc -l | tr -d ' ')
_quiesce "$P"
echo "observed: bridge_spawn_events=$SPAWNS live_bridges=$BRIDGES opencode=$OC cline=$CL"
if [ "$SPAWNS" -le 1 ] && [ "$BRIDGES" -le 1 ] && [ "$OC" -eq 0 ] && [ "$CL" -eq 0 ]; then
  echo "AT-003 PASS: lazy-start 生效且无泄漏"
else
  echo "AT-003 FAIL: spawns=$SPAWNS bridges=$BRIDGES opencode=$OC cline=$CL"
fi
