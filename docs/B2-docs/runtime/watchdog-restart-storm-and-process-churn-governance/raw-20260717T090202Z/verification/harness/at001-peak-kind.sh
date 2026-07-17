#!/bin/bash
# AT-001: 沙箱 — cycle 记录不触发 peak;death 记录触发;文档口径在位
set -u
F="$(pwd)/docs/system/workspace/scripts/runtime/freely"
CL="$(pwd)/docs/system/workspace/three-loop-capability-lifecycle.md"
TMP=$(mktemp -d); trap 'rm -rf "$TMP"' EXIT
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
} > "$TMP/h.sh"
R1=$(bash -c '
  source "'"$TMP"'/harness_na" 2>/dev/null; source "'"$TMP"'/h.sh" 2>/dev/null
  for i in 1 2 3 4 5; do update_restart_storm_window "d" "$(date +%s)" 3 cycle 2>/dev/null || update_restart_storm_window "d" "$(date +%s)" 3 2>/dev/null; done
  stats="$(restart_storm_window_stats "d")"
  restart_storm_signal_reason_for_window "${stats%%|*}" "${stats##*|}" 2>/dev/null || echo none
')
R2=$(bash -c '
  source "'"$TMP"'/h.sh" 2>/dev/null
  rm -f "$RUN_DIR/restart-storm-window.tsv" 2>/dev/null
  for i in 1 2 3; do record_supervisor_death_for_storm_window "d" >/dev/null 2>&1; done
  stats="$(restart_storm_window_stats "d")"
  restart_storm_signal_reason_for_window "${stats%%|*}" "${stats##*|}" 2>/dev/null || echo none
')
DOC=0; grep -q "peak.*death\|death.*峰\|死亡.*峰" "$CL" && DOC=1
echo "observed: cycle_reason=$R1 death_reason=$R2 doc=$DOC"
if [ "$R1" = "none" ] && [ "$R2" = "process_churn_peak_threshold" ] && [ "$DOC" -eq 1 ]; then
  echo "AT-001 PASS: cycle 不触发/death 触发/口径已文档化"
else
  echo "AT-001 FAIL: cycle=$R1 death=$R2 doc=$DOC"
fi
