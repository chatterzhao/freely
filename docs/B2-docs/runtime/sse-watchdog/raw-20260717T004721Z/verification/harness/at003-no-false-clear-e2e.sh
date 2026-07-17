#!/usr/bin/env bash
# AT-003: 已验证存活的 sse-watchdog pid 不被 self-heal 误清
# 方法: 起 daemon → 确认 sse pid 存活 → 触发 self-heal(live-status) → 断言无针对该活 pid 的清除事件
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
"$P/bin/freely" daemon start --project "$P" --task-mode wait >/dev/null 2>&1
sleep 30
SSE_PID=$(cat "$P/.freely/run/sse-watchdog.pid" 2>/dev/null || true)
if [ -z "$SSE_PID" ] || ! kill -0 "$SSE_PID" 2>/dev/null; then
  # pid 文件已被误清但进程可能还活着——用进程发现兜底
  SSE_PID=$(pgrep -f "sse-watchdog.sh --project $P" | head -1)
fi
if [ -z "$SSE_PID" ] || ! kill -0 "$SSE_PID" 2>/dev/null; then
  _quiesce "$P"; echo "AT-003 FAIL: 无存活 sse-watchdog 可测(inconclusive)"; exit 0
fi
M1=$(wc -l < "$EV" | tr -d ' ')
"$P/bin/freely" live-status --project "$P" >/dev/null 2>&1   # 触发 trigger=live_status 的 self-heal
sleep 2
CLEARS=$(sed -n "$((M1+1)),\$p" "$EV" | grep "startup_self_heal_stale_pid_cleared" | grep "role=sse_watchdog" | grep -c "pid=$SSE_PID" || true)
ALIVE=0; kill -0 "$SSE_PID" 2>/dev/null && ALIVE=1
PIDFILE_OK=0; [ "$(cat "$P/.freely/run/sse-watchdog.pid" 2>/dev/null)" = "$SSE_PID" ] && PIDFILE_OK=1
_quiesce "$P"
echo "observed: live_sse_pid=$SSE_PID false_clears=$CLEARS still_alive=$ALIVE pidfile_intact=$PIDFILE_OK"
if [ "$CLEARS" -eq 0 ] && [ "$ALIVE" -eq 1 ] && [ "$PIDFILE_OK" -eq 1 ]; then
  echo "AT-003 PASS: 活 sse-watchdog 未被误清"
else
  echo "AT-003 FAIL: clears=$CLEARS alive=$ALIVE pidfile=$PIDFILE_OK"
fi
