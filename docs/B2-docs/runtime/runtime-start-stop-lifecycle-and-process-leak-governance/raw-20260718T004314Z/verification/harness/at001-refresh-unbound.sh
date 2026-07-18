#!/usr/bin/env bash
# AT-001: sourced probe 调 refresh —— 修复版正常返回（RED 用 HEAD 版脚本复现 unbound 死亡）
# usage: at001-refresh-unbound.sh <runtime_freely_script> <main_project_root>
set -uo pipefail
S="$1"; P="$2"
out=$(bash <<SH 2>&1
source "$S"
if manager_worker_launch_state_refresh_for_status "$P"; then :; fi
echo PROBE_END
SH
)
rc=$?
echo "$out" | grep -q "unbound variable" && { echo "  unbound variable reproduced"; echo "AT001_RESULT: FAIL"; exit 1; }
echo "$out" | grep -q "PROBE_END" || { echo "  probe died (rc=$rc) without unbound msg"; echo "AT001_RESULT: FAIL"; exit 1; }
echo "  probe survived refresh"
echo "AT001_RESULT: PASS"
