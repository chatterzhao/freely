#!/usr/bin/env bash
# AT-005 harness: storm window 记录 supervisor 死亡并在阈值处触发信号
# 两部分: (a) 静态断言 ensure-manager 侧存在死亡记录调用点
#         (b) 行为断言: 提取 storm window 函数,模拟 N 次死亡记录,阈值处 reason 非空
set -u
P="$(pwd)"
F="$P/docs/system/workspace/scripts/runtime/freely"
FAIL=0
# (a) 静态: record_supervisor_death_for_storm_window 存在且被 ensure_manager 路径调用
if ! grep -q "record_supervisor_death_for_storm_window()" "$F"; then
  echo "part-a FAIL: record_supervisor_death_for_storm_window 函数不存在"; FAIL=1
elif ! awk '/^ensure_manager_once\(\)/,/^}/' "$F" | grep -q "record_supervisor_death_for_storm_window\|restart_manager_supervisor_preserving_handoff"; then
  echo "part-a FAIL: ensure_manager_once 未接入死亡记录/teardown 路径"; FAIL=1
else
  echo "part-a PASS"
fi
# (b) 行为: 提取 update_restart_storm_window + restart_storm_signal_reason_for_window 到沙箱执行
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
{
  echo 'set -u'
  echo "RUN_DIR=\"$TMP/run\"; mkdir -p \"\$RUN_DIR\""
  echo 'run_dir_for_project() { echo "$RUN_DIR"; }'
  echo 'runtime_now_epoch() { date +%s; }'
  echo 'runtime_active_process_count_for_project() { echo 3; }'
  echo 'RESTART_STORM_WINDOW_SECS=30'
  # 阈值取实现真源的 config 默认（从 config init 行提取）
  grep -oE 'RESTART_STORM_COUNT[ ]*=[ ]*[0-9]+' "$F" | head -1
  grep -oE 'PROCESS_CHURN_PEAK[ ]*=[ ]*[0-9]+' "$F" | head -1
  awk '/^update_restart_storm_window\(\)/,/^}/' "$F"
  awk '/^restart_storm_signal_reason_for_window\(\)/,/^}/' "$F"
  awk '/^record_supervisor_death_for_storm_window\(\)/,/^}/' "$F"
} > "$TMP/harness.sh"
COUNT=$(grep -oE 'RESTART_STORM_COUNT[ ]*=[ ]*[0-9]+' "$F" | head -1 | grep -oE '[0-9]+')
COUNT=${COUNT:-10}
REASON=$(bash -c '
  source "'"$TMP"'/harness.sh" 2>/dev/null
  for i in $(seq 1 '"$COUNT"'); do
    if declare -f record_supervisor_death_for_storm_window >/dev/null; then
      record_supervisor_death_for_storm_window "dummy-project" 2>/dev/null
    else
      update_restart_storm_window "dummy-project" 2>/dev/null
    fi
  done
  restart_storm_signal_reason_for_window "dummy-project" 2>/dev/null
' 2>/dev/null)
if [ -n "$REASON" ]; then
  echo "part-b PASS: 阈值 $COUNT 次死亡记录后 storm reason='$REASON'"
else
  echo "part-b FAIL: $COUNT 次记录后 storm reason 为空(阈值不可达或记录未生效)"; FAIL=1
fi
[ "$FAIL" -eq 0 ] && echo "AT-005 PASS" || echo "AT-005 FAIL"
