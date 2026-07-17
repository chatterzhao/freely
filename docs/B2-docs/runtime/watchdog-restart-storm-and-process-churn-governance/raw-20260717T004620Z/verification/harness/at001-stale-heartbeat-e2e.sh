#!/usr/bin/env bash
# AT-001 harness: stale heartbeat 场景下新生 supervisor 不被误杀、无双 daemon
# 用法: 在 test-pre-merge 工位根目录执行  bash <this>  （需先 pre-init-runtime）
# PASS 条件: 启动后 45s 窗口内 0 次 daemon_signal_ignored 且 daemon-run 进程数 ≤1
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

_quiesce "$P"
EV="$P/.freely/logs/runtime-events.log"
mkdir -p "$P/.freely/run" "$P/.freely/logs"; touch "$EV"
# 预置 stale heartbeat（mtime 远早于即将启动的 supervisor）
touch -t 202607010000 "$P/.freely/run/supervisor-heartbeat"
rm -f "$P/.freely/run/stop.requested"
M0=$(wc -l < "$EV" | tr -d ' ')
"$P/bin/freely" daemon start --project "$P" --task-mode wait >/dev/null 2>&1
sleep 45
NEW="$(sed -n "$((M0+1)),\$p" "$EV")"
IGN=$(printf '%s\n' "$NEW" | grep -c "daemon_signal_ignored" || true)
STARTS=$(printf '%s\n' "$NEW" | grep -c "event=supervisor_started" || true)
DRC=$(pgrep -f "daemon-run --project $P" | wc -l | tr -d ' ')
CLEAN=$(printf '%s\n' "$NEW" | grep -c "event=supervisor_cleanup " || true)
_quiesce "$P"
echo "observed: ignored_TERM=$IGN supervisor_started=$STARTS daemon_run_procs=$DRC cleanups=$CLEAN"
if [ "$IGN" -eq 0 ] && [ "$DRC" -le 1 ] && [ "$STARTS" -ge 1 ] && [ "$CLEAN" -le 1 ]; then
  echo "AT-001 PASS: newborn survived stale heartbeat, single daemon"
else
  echo "AT-001 FAIL: ignored=$IGN starts=$STARTS daemon_runs=$DRC cleanups=$CLEAN"
fi
