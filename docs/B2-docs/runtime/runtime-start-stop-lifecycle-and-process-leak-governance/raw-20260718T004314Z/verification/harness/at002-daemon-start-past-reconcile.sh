#!/usr/bin/env bash
# AT-002: bash -n 语法 + daemon status 穿过 L25325 无防护 refresh 调用点
# 判据：refresh 点之后的输出字段（intake_active_items）出现 = 未在 reconcile 处死亡
# usage: at002-daemon-start-past-reconcile.sh <runtime_freely_script> <main_project_root>
set -uo pipefail
S="$1"; P="$2"
bash -n "$S" || { echo "AT002_RESULT: FAIL (syntax)"; exit 1; }
out=$(cd "$P" && bash "$S" daemon status 2>&1); rc=$?
echo "  daemon status rc=$rc"
echo "$out" | grep -q "unbound variable" && { echo "  unbound variable in output"; echo "AT002_RESULT: FAIL"; exit 1; }
if echo "$out" | grep -q "intake_active_items"; then
  echo "  post-reconcile fields present"
  echo "AT002_RESULT: PASS"; exit 0
fi
echo "  output ends before post-reconcile fields (died at refresh point)"
echo "$out" | tail -2 | sed 's/^/    /'
echo "AT002_RESULT: FAIL"; exit 1
