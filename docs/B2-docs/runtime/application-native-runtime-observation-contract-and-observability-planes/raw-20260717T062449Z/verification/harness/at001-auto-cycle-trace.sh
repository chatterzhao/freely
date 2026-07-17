#!/bin/bash
# AT-001: auto 周期 E2E — L041 时差 ≤10s 且 L042 OUT to 为单值
set -u
Q="$(pwd)"
_quiesce() {
  "$Q/bin/freely" stop --project "$Q" >/dev/null 2>&1 || true; sleep 2
  for pat in "daemon-run --project $Q" "ensure-manager --project $Q" "ensure-interruption-dispatch --project $Q" "sse-watchdog.sh --project $Q" "watchdog_sse.py --project $Q" "acp-bridge.py start --project $Q"; do pkill -f "$pat" 2>/dev/null || true; done
  for i in 1 2 3 4 5 6; do pgrep -f "project $Q" | grep -qv "^$$\$" || break; sleep 2; done
  rm -f "$Q/.freely/run/stop.requested"
}
_quiesce "$Q"
TR="$Q/.freely/logs/lifecycle-trace.log"; mkdir -p "$Q/.freely/logs"; touch "$TR"
T0=$(wc -l < "$TR" | tr -d ' ')
"$Q/bin/freely" daemon start --project "$Q" --task-mode auto >/dev/null 2>&1
# 等一个完整 cycle（L042 出现,≤420s）
L42=""
for i in $(seq 1 84); do sleep 5; L42=$(sed -n "$((T0+1)),\$p" "$TR" | grep "ph=OUT me=A-L042" | tail -1); [ -n "$L42" ] && break; done
NEW="$(sed -n "$((T0+1)),\$p" "$TR")"
_quiesce "$Q"
B_TS=$(printf '%s\n' "$NEW" | grep "ph=IN me=A-L040" | head -1 | awk '{print $1}')
O_TS=$(printf '%s\n' "$NEW" | grep "ph=IN me=A-L041" | head -1 | awk '{print $1}')
D=-1
if [ -n "$B_TS" ] && [ -n "$O_TS" ]; then
  BE=$(date -j -u -f "%Y-%m-%dT%H:%M:%SZ" "$B_TS" +%s 2>/dev/null || echo 0)
  OE=$(date -j -u -f "%Y-%m-%dT%H:%M:%SZ" "$O_TS" +%s 2>/dev/null || echo 0)
  D=$((OE-BE))
fi
TO=$(printf '%s' "$L42" | grep -oE "to=[^ ]+" | head -1)
echo "observed: l041_delta=${D}s l042_out='$TO'"
OK=1
[ "$D" -ge 0 ] && [ "$D" -le 10 ] || { echo "L041 时差超限或缺失"; OK=0; }
printf '%s' "$TO" | grep -qE '^to=A-L[0-9]+$|^to=TERM$' || { echo "L042 OUT 非单值"; OK=0; }
[ "$OK" -eq 1 ] && echo "AT-001 PASS" || echo "AT-001 FAIL"
