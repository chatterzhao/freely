#!/bin/bash
# AT-002: stop 场景 — cleanup 链 L090/L092 OUT ok=1 且 to 单值
set -u
Q="$(pwd)"
_quiesce() {
  "$Q/bin/freely" stop --project "$Q" >/dev/null 2>&1 || true; sleep 2
  for pat in "daemon-run --project $Q" "ensure-manager --project $Q" "ensure-interruption-dispatch --project $Q" "sse-watchdog.sh --project $Q" "watchdog_sse.py --project $Q" "acp-bridge.py start --project $Q"; do pkill -f "$pat" 2>/dev/null || true; done
  for i in 1 2 3 4 5 6; do pgrep -f "project $Q" | grep -qv "^$$\$" || break; sleep 2; done
  rm -f "$Q/.freely/run/stop.requested"
}
_quiesce "$Q"
TR="$Q/.freely/logs/lifecycle-trace.log"; touch "$TR"; T0=$(wc -l < "$TR" | tr -d ' ')
"$Q/bin/freely" daemon start --project "$Q" --task-mode wait >/dev/null 2>&1
for i in $(seq 1 30); do sleep 1; [ -f "$Q/.freely/run/supervisor.pid" ] && kill -0 "$(cat $Q/.freely/run/supervisor.pid)" 2>/dev/null && break; done
sleep 3
"$Q/bin/freely" stop --project "$Q" >/dev/null 2>&1; sleep 5
NEW="$(sed -n "$((T0+1)),\$p" "$TR")"
_quiesce "$Q"
L90=$(printf '%s\n' "$NEW" | grep "ph=OUT me=A-L090" | tail -1)
L92=$(printf '%s\n' "$NEW" | grep "ph=OUT me=A-L092" | tail -1)
OK=1
for L in "$L90" "$L92"; do
  [ -n "$L" ] || { echo "缺 OUT 行"; OK=0; continue; }
  printf '%s' "$L" | grep -q "ok=1" || { echo "ok!=1: $L"; OK=0; }
  printf '%s' "$L" | grep -oE "to=[^ ]+" | grep -qE '^to=A-L[0-9]+$|^to=TERM$' || { echo "to 非单值: $L"; OK=0; }
done
echo "observed L090: ${L90:-none}"
echo "observed L092: ${L92:-none}"
[ "$OK" -eq 1 ] && echo "AT-002 PASS" || echo "AT-002 FAIL"
