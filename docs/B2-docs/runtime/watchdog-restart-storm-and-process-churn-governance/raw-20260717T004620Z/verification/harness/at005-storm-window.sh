#!/usr/bin/env bash
# AT-005 harness: storm window 记录 supervisor 死亡并在阈值处触发信号
# 两部分: (a) 静态断言 ensure-manager 侧存在死亡记录调用点
#         (b) 行为断言: 提取 storm window 函数,模拟阈值次数死亡记录,reason 非空
set -u
P="$(pwd)"
F="$P/docs/system/workspace/scripts/runtime/freely"
FAIL=0
# (a) 静态: record_supervisor_death_for_storm_window 存在且被 ensure_manager 路径调用
if ! grep -q "record_supervisor_death_for_storm_window()" "$F"; then
  echo "part-a FAIL: record_supervisor_death_for_storm_window 函数不存在"; FAIL=1
elif ! awk '/^ensure_manager_once\(\)/,/^}/' "$F" | grep -q "record_supervisor_death_for_storm_window"; then
  echo "part-a FAIL: ensure_manager_once 未接入死亡记录路径"; FAIL=1
else
  echo "part-a PASS"
fi
# (b) 行为: 提取相关函数到沙箱执行——阈值次数记录后 reason 必须非空
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
{
  echo 'set -u'
  echo "RUN_DIR=\"$TMP/run\"; mkdir -p \"\$RUN_DIR\""
  echo 'run_dir_for_project() { echo "$RUN_DIR"; }'
  echo 'runtime_now_epoch() { date +%s; }'
  echo 'runtime_active_process_count_for_project() { echo 3; }'
  echo 'record_restart_storm_signal() { :; }'
  echo 'append_runtime_event() { :; }'
  awk '/^restart_storm_window_file\(\)/,/^}/' "$F"
  awk '/^update_restart_storm_window\(\)/,/^}/' "$F"
  awk '/^restart_storm_window_stats\(\)/,/^}/' "$F"
  awk '/^restart_storm_signal_reason_for_window\(\)/,/^}/' "$F"
  awk '/^record_supervisor_death_for_storm_window\(\)/,/^}/' "$F"
} > "$TMP/harness.sh"
COUNT=$(grep -oE 'RESTART_STORM_COUNT[ ]*=[ ]*[0-9]+' "$F" | head -1 | grep -oE '[0-9]+')
COUNT=${COUNT:-10}
REASON=$(bash -c '
  source "'"$TMP"'/harness.sh" 2>/dev/null
  if ! declare -f record_supervisor_death_for_storm_window >/dev/null; then
    exit 0
  fi
  for i in $(seq 1 '"$COUNT"'); do
    record_supervisor_death_for_storm_window "dummy-project" >/dev/null 2>&1
  done
  stats="$(restart_storm_window_stats "dummy-project")"
  restart_storm_signal_reason_for_window "${stats%%|*}" "${stats##*|}" 2>/dev/null
' 2>/dev/null)
if [ -n "$REASON" ]; then
  echo "part-b PASS: 阈值 $COUNT 次死亡记录后 storm reason='$REASON'"
else
  echo "part-b FAIL: $COUNT 次记录后 storm reason 为空(阈值不可达或记录未生效)"; FAIL=1
fi
[ "$FAIL" -eq 0 ] && echo "AT-005 PASS" || echo "AT-005 FAIL"
