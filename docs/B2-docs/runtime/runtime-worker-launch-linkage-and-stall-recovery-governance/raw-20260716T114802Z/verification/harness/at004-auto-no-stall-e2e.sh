#!/usr/bin/env bash
# AT-004: 真实 auto 启动 150s 观察窗内，AI 存活期间 0 次 stall recovery 误触发
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
"$P/bin/freely" daemon start --project "$P" --task-mode auto >/dev/null 2>&1
sleep 150
NEW="$(sed -n "$((M0+1)),\$p" "$EV")"
STALLS=$(printf '%s\n' "$NEW" | grep -c "runtime_stalled_ai_recovery_triggered" || true)
LAUNCH=$(printf '%s\n' "$NEW" | grep -c "event=ai_launch_begin" || true)
RC1=$(printf '%s\n' "$NEW" | grep -c "exit_reason=ai_exit_rc_1" || true)
_quiesce "$P"
echo "observed: stall_triggers=$STALLS ai_launched=$LAUNCH ai_rc1_exits=$RC1"
if [ "$STALLS" -eq 0 ] && [ "$LAUNCH" -ge 1 ]; then echo "AT-004 PASS: 150s 窗口无 stall 误触发"; else echo "AT-004 FAIL: stalls=$STALLS launched=$LAUNCH"; fi
