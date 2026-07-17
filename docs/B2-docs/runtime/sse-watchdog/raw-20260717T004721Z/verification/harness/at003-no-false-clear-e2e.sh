#!/usr/bin/env bash
# AT-003: 真实 daemon 启动窗口内 0 次 sse_watchdog 误清事件
set -u
P="$(pwd)"
_quiesce() {
  local proj="$1"
  "$proj/bin/freely" stop --project "$proj" >/dev/null 2>&1 || true
  sleep 2
  for pat in "daemon-run --project $proj" "ensure-manager --project $proj" "ensure-interruption-dispatch --project $proj" "sse-watchdog.sh --project $proj" "watchdog_sse.py --project $proj" "acp-bridge.py start --project $proj"; do
    pkill -f "$pat" 2>/dev/null || true
  done
  for i in 1 2 3 4 5 6 7 8; do pgrep -f "project $proj" | grep -qv "^$$\$" || break; sleep 2; done
  rm -f "$proj/.freely/run/stop.requested"
}
_quiesce "$P"
EV="$P/.freely/logs/runtime-events.log"; mkdir -p "$P/.freely/logs"; touch "$EV"
M0=$(wc -l < "$EV" | tr -d ' ')
"$P/bin/freely" daemon start --project "$P" --task-mode wait >/dev/null 2>&1
sleep 45
CLEARS=$(sed -n "$((M0+1)),\$p" "$EV" | grep -c "startup_self_heal_stale_pid_cleared.*role=sse_watchdog" || true)
STARTS=$(sed -n "$((M0+1)),\$p" "$EV" | grep -c "event=supervisor_started" || true)
_quiesce "$P"
echo "observed: sse_false_clears=$CLEARS supervisor_started=$STARTS"
if [ "$CLEARS" -eq 0 ] && [ "$STARTS" -ge 1 ]; then echo "AT-003 PASS: 无 sse 误清事件"; else echo "AT-003 FAIL: clears=$CLEARS starts=$STARTS"; fi
