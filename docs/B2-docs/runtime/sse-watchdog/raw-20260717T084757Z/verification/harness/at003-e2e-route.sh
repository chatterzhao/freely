#!/bin/bash
# AT-003: 真实 daemon + chat 触发 SSE 路由 — 无 NameError 且路由完成
set -u
Q="$(pwd)"
_quiesce() {
  "$Q/bin/freely" stop --project "$Q" >/dev/null 2>&1 || true; sleep 2
  for pat in "daemon-run --project $Q" "ensure-manager --project $Q" "ensure-interruption-dispatch --project $Q" "sse-watchdog.sh --project $Q" "watchdog_sse.py --project $Q" "acp-bridge.py start --project $Q"; do pkill -f "$pat" 2>/dev/null || true; done
  for i in 1 2 3 4 5 6; do pgrep -f "project $Q" | grep -qv "^$$\$" || break; sleep 2; done
  rm -f "$Q/.freely/run/stop.requested"
}
_quiesce "$Q"
WL="$Q/.freely/run/watchdog-sse.log"; : > "$WL" 2>/dev/null || true
"$Q/bin/freely" daemon start --project "$Q" --task-mode wait >/dev/null 2>&1
for i in $(seq 1 30); do sleep 1; pgrep -f "watchdog_sse.py --project $Q" >/dev/null && break; done
sleep 3
# 直接注入 A2A input-required 事件(SSE 全局流→watchdog 路由的确定性触发)
AT=$(python3 "$Q/docs/system/workspace/scripts/runtime/a2a_task.py" --project "$Q" create --raw-key route-probe --message "harness 路由探针" --agent-id worker 2>/dev/null | python3 -c "import json,sys; print(json.load(sys.stdin).get('task_id',''))" 2>/dev/null)
[ -n "$AT" ] && python3 "$Q/docs/system/workspace/scripts/runtime/a2a_task.py" --project "$Q" update --task-id "$AT" --state input-required --reason needs-review:code --from-agent worker_01 >/dev/null 2>&1
sleep 12
NE=$(grep -c "_get_agent_slot' is not defined" "$WL" || true)
RT=$(grep -cE "routing to (manager|worker|reviewer)" "$WL" || true)
_quiesce "$Q"
echo "observed: nameerror=$NE routes_logged=$RT"
if [ "$NE" -eq 0 ] && [ "$RT" -ge 1 ]; then echo "AT-003 PASS"; else echo "AT-003 FAIL: nameerror=$NE routes=$RT"; fi
