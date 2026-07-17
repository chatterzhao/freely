#!/usr/bin/env bash
# AT-002 harness: heartbeat touch 子进程在 supervisor_started 后 ≤3s 开始更新
# 用法: 在 test-pre-merge 工位根目录执行。PASS: heartbeat mtime 与 supervisor_started 事件时间差 ≤3s
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
HB="$P/.freely/run/supervisor-heartbeat"
rm -f "$HB" "$P/.freely/run/stop.requested"; mkdir -p "$P/.freely/logs"; touch "$EV"
M0=$(wc -l < "$EV" | tr -d ' ')
"$P/bin/freely" daemon start --project "$P" --task-mode wait >/dev/null 2>&1
# 等 supervisor_started 出现（≤60s）
STARTED_TS=""
for i in $(seq 1 60); do
  STARTED_TS=$(sed -n "$((M0+1)),\$p" "$EV" | grep "event=supervisor_started" | head -1 | awk '{print $1}')
  [ -n "$STARTED_TS" ] && break
  sleep 1
done
if [ -z "$STARTED_TS" ]; then "$P/bin/freely" stop --project "$P" >/dev/null 2>&1; echo "AT-002 FAIL: supervisor_started never appeared"; exit 0; fi
sleep 4  # 给 3s 承诺 + 1s 容差
STARTED_EPOCH=$(date -j -u -f "%Y-%m-%dT%H:%M:%SZ" "$STARTED_TS" +%s 2>/dev/null || echo 0)
HB_EPOCH=$(stat -f %m "$HB" 2>/dev/null || echo 0)
DELTA=$((HB_EPOCH - STARTED_EPOCH))
_quiesce "$P"
echo "observed: supervisor_started=$STARTED_TS heartbeat_mtime_delta=${DELTA}s"
if [ "$HB_EPOCH" -gt 0 ] && [ "$DELTA" -ge -1 ] && [ "$DELTA" -le 3 ]; then
  echo "AT-002 PASS: heartbeat live within 3s of supervisor_started"
else
  echo "AT-002 FAIL: delta=${DELTA}s (heartbeat 子进程未在 3s 内启动)"
fi
