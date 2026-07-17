#!/usr/bin/env bash
# AT-003: watchdog 重拉路径的 A-L240 OUT 必须带 to=A-L010 ok=1
# 方法: daemon start → kill -9 supervisor(绕过 cleanup) → ensure-manager 重拉 → 取最新 L240 OUT
set -u
P="$(pwd)"
TR="$P/.freely/logs/lifecycle-trace.log"
"$P/bin/freely" stop --project "$P" >/dev/null 2>&1; sleep 2
pkill -f "project $P" 2>/dev/null; sleep 2; rm -f "$P/.freely/run/stop.requested"
mkdir -p "$P/.freely/logs"; touch "$TR"; T0=$(wc -l < "$TR" | tr -d ' ')
"$P/bin/freely" daemon start --project "$P" --task-mode wait >/dev/null 2>&1
# 等 supervisor 起来
SUP=""
for i in $(seq 1 40); do sleep 1; SUP=$(cat "$P/.freely/run/supervisor.pid" 2>/dev/null); [ -n "$SUP" ] && kill -0 "$SUP" 2>/dev/null && break; done
if [ -z "$SUP" ]; then echo "AT-003 FAIL: supervisor 未启动(inconclusive)"; exit 0; fi
sleep 3
kill -9 "$SUP" 2>/dev/null   # 猝死,绕过 cleanup → watchdog 应检出并重拉
# 等 L240 出现(≤40s)
LINE=""
for i in $(seq 1 40); do
  sleep 1
  LINE=$(sed -n "$((T0+1)),\$p" "$TR" | grep "ph=OUT me=A-L240" | tail -1)
  [ -n "$LINE" ] && break
done
"$P/bin/freely" stop --project "$P" >/dev/null 2>&1; sleep 2; pkill -f "project $P" 2>/dev/null
echo "L240_OUT: $LINE"
if [ -z "$LINE" ]; then echo "AT-003 FAIL: watchdog 未打出 L240(inconclusive)";
elif printf '%s' "$LINE" | grep -q "to=A-L010 ok=1"; then echo "AT-003 PASS";
else echo "AT-003 FAIL: to/ok 仍为 UNSET/0"; fi
