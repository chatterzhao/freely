#!/bin/bash
# AT-003: 运行中污染 develop → 事件出现且去抖
set -u
Q="$(pwd)"
_quiesce() {
  "$Q/bin/freely" stop --project "$Q" >/dev/null 2>&1 || true; sleep 2
  for pat in "daemon-run --project $Q" "ensure-manager --project $Q" "ensure-interruption-dispatch --project $Q" "sse-watchdog.sh --project $Q" "watchdog_sse.py --project $Q" "acp-bridge.py start --project $Q"; do pkill -f "$pat" 2>/dev/null || true; done
  for i in 1 2 3 4 5 6; do pgrep -f "project $Q" | grep -qv "^$$\$" || break; sleep 2; done
  rm -f "$Q/.freely/run/stop.requested"
}
_quiesce "$Q"
EV="$Q/.freely/logs/runtime-events.log"; mkdir -p "$Q/.freely/logs"; touch "$EV"; M0=$(wc -l < "$EV" | tr -d ' ')
"$Q/bin/freely" daemon start --project "$Q" --task-mode wait >/dev/null 2>&1
for i in $(seq 1 30); do sleep 1; [ -f "$Q/.freely/run/supervisor.pid" ] && kill -0 "$(cat $Q/.freely/run/supervisor.pid)" 2>/dev/null && break; done
echo "harness-taint $(date +%s)" >> "$Q/AGENTS.md"   # 污染一个 tracked 文件
sleep 25   # 覆盖 ≥1 个主循环周期
DET=$(sed -n "$((M0+1)),\$p" "$EV" | grep -c "protected_root_dirty_detected" || true)
sleep 25   # 再等一轮,同指纹应去抖
DET2=$(sed -n "$((M0+1)),\$p" "$EV" | grep -c "protected_root_dirty_detected" || true)
git -C "$Q" checkout -- AGENTS.md
_quiesce "$Q"
echo "observed: detected=$DET after_debounce=$DET2"
if [ "$DET" -ge 1 ] && [ "$DET2" -eq "$DET" ]; then echo "AT-003 PASS"; else echo "AT-003 FAIL: det=$DET det2=$DET2"; fi
