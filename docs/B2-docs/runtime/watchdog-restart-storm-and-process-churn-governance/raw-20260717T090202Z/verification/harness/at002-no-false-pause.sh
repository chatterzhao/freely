#!/bin/bash
# AT-002: 真实 daemon auto 短窗(一个 AI cycle 后) — 0 次 restart_storm_pause
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
rm -f "$Q/.freely/run/restart-storm-window.tsv"
"$Q/bin/freely" daemon start --project "$Q" --task-mode auto >/dev/null 2>&1
# 等第一个 AI cycle 完成(storm window 记录点),≤420s
for i in $(seq 1 84); do sleep 5; sed -n "$((M0+1)),\$p" "$EV" | grep -q "ai_cycle_finished" && break; done
sleep 8
PAUSES=$(sed -n "$((M0+1)),\$p" "$EV" | grep -c "restart_storm_pause" || true)
STARTS=$(sed -n "$((M0+1)),\$p" "$EV" | grep -c "ai_cycle_finished" || true)
_quiesce "$Q"
echo "observed: storm_pauses=$PAUSES cycles_finished=$STARTS"
if [ "$PAUSES" -eq 0 ] && [ "$STARTS" -ge 1 ]; then echo "AT-002 PASS: 零误 pause"; else echo "AT-002 FAIL: pauses=$PAUSES"; fi
