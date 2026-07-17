#!/usr/bin/env bash
# AT-007 harness: 回归端到端 — stale heartbeat 前置下 task_mode=auto 完整链
# PASS: L010→L020→L021→L022→L040 全部出现 且 0 次 daemon_signal_ignored 且 daemon-run ≤1
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
  [ -n "$hash" ] && rm -f /tmp/freely-acp-${hash}-*.sock /tmp/freely-acp-${hash}-*.pid* 2>/dev/null
  for i in 1 2 3 4 5 6 7 8; do
    pgrep -f "project $proj" | grep -qv "^$$\$" || break
    sleep 2
  done
  rm -f "$proj/.freely/run/stop.requested"
}

_top_level_daemon_runs() {
  # 只数顶层 daemon-run：排除 argv 相同的 fork 子进程（如 heartbeat 子 shell，其
  # PPID 在匹配集内）。真正的第二个 daemon（nohup+disown, PPID=1）仍会被计入。
  local proj="$1" pids pid pp n=0
  pids=$(pgrep -f "daemon-run --project $proj" 2>/dev/null || true)
  for pid in $pids; do
    pp=$(ps -o ppid= -p "$pid" 2>/dev/null | tr -d " ")
    if [ -n "$pp" ] && printf "%s\n" $pids | grep -q "^$pp$"; then continue; fi
    n=$((n+1))
  done
  echo "$n"
}

_quiesce "$P"
EV="$P/.freely/logs/runtime-events.log"
TR="$P/.freely/logs/lifecycle-trace.log"
mkdir -p "$P/.freely/run" "$P/.freely/logs"; touch "$EV" "$TR"
touch -t 202607010000 "$P/.freely/run/supervisor-heartbeat"
rm -f "$P/.freely/run/stop.requested"
M0=$(wc -l < "$EV" | tr -d ' '); T0=$(wc -l < "$TR" | tr -d ' ')
"$P/bin/freely" daemon start --project "$P" --task-mode auto >/dev/null 2>&1
# 轮询 ≤240s 等 L040
OK=0
for i in $(seq 1 48); do
  sleep 5
  if sed -n "$((T0+1)),\$p" "$TR" | grep -q "checkpoint=L040"; then OK=1; break; fi
done
NEWEV="$(sed -n "$((M0+1)),\$p" "$EV")"
NEWTR="$(sed -n "$((T0+1)),\$p" "$TR")"
IGN=$(printf '%s\n' "$NEWEV" | grep -c "daemon_signal_ignored" || true)
DRC=$(_top_level_daemon_runs "$P")
CHAIN=1
for cp in L010 L020 L021 L022 L040; do
  printf '%s\n' "$NEWTR" | grep -q "checkpoint=$cp" || { CHAIN=0; echo "missing checkpoint: $cp"; }
done
_quiesce "$P"
echo "observed: chain_complete=$CHAIN L040_within_240s=$OK ignored_TERM=$IGN daemon_runs=$DRC"
if [ "$CHAIN" -eq 1 ] && [ "$OK" -eq 1 ] && [ "$IGN" -eq 0 ] && [ "$DRC" -le 1 ]; then
  echo "AT-007 PASS: auto 模式全链走通且无误杀/双 daemon"
else
  echo "AT-007 FAIL: chain=$CHAIN l040=$OK ignored=$IGN daemon_runs=$DRC"
fi
