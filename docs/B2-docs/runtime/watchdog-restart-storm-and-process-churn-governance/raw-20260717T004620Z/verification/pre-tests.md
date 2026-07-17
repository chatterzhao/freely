# Pre-Tests: supervisor 生死判定一体收口
- issue_id: I-20260717T004620Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: stale heartbeat 场景下新生 supervisor 不被误杀、不出现双 daemon（C1a+C2b）
- acceptance_target: 预置 stale heartbeat 后 daemon start，45s 窗口内 0 次 daemon_signal_ignored 且 daemon-run 进程 ≤1
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T004620Z-supervisor-liveness-storm
- required_evidence: harness 输出 observed 行 + PASS 判定，evidence log 落盘
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-1.log
- test_command: bash docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/harness/at001-stale-heartbeat-e2e.sh
- expected_output: "AT-001 PASS: newborn survived stale heartbeat, single daemon"
- expected_RED_output: "AT-001 FAIL: ignored>=1 或 daemon_runs>=2（复现 2026-07-17T00:16:27Z daemon_signal_ignored + 双 daemon）"
- actual_RED_output: observed: ignored_TERM=1 supervisor_started=1 daemon_run_procs=2 cleanups=0 → AT-001 FAIL: ignored=1 starts=1 daemon_runs=2 cleanups=0（复现 ensure-manager 对新生 supervisor 发 TERM 被忽略 + 双 daemon）
- actual_output: observed: ignored_TERM=0 supervisor_started=1 daemon_run_procs=1 cleanups=0 → AT-001 PASS: newborn survived stale heartbeat, single daemon
- evidence_file: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 在 test-pre-merge 工位真实 daemon start 复现（与 2026-07-17T00:16/00:33 两次生产复现同法）：backdate heartbeat → start → 观察 TERM 忽略事件与 daemon-run 计数

### acceptance-2
- id: AT-002
- requirement: heartbeat 子进程在 supervisor 启动序列中先于 bridge init 启动（C1b）
- acceptance_target: 源码顺序——heartbeat 后台子进程启动块位于 ACP bridge init 块之前（消除依赖 bridge 冷启动时长的裸奔窗口）；辅助证据：真实启动时 heartbeat mtime 与 supervisor_started 差 ≤3s
- testing_layer: integration
- target_environment: fix/raw-20260717T004620Z-supervisor-liveness-storm
- required_evidence: 源码顺序断言 PASS + at002 harness 时延实测（辅助）
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-2.log
- test_command: |
  F=docs/system/workspace/scripts/runtime/freely
  HB_LINE=$(grep -nF '_heartbeat_bg_pid=' "$F" | head -1 | cut -d: -f1)
  BR_LINE=$(grep -n "ACP bridge lifecycle: start one bridge per unique base_tool" "$F" | head -1 | cut -d: -f1)
  echo "heartbeat_block_line=$HB_LINE bridge_init_line=$BR_LINE"
  if [ -n "$HB_LINE" ] && [ -n "$BR_LINE" ] && [ "$HB_LINE" -lt "$BR_LINE" ]; then echo "PASS: heartbeat 先于 bridge init"; else echo "FAIL: heartbeat 块在 bridge init 之后(窗口依赖 bridge 冷启动时长)"; fi
- expected_output: "PASS: heartbeat 先于 bridge init"
- expected_RED_output: "FAIL: heartbeat 块在 bridge init 之后(窗口依赖 bridge 冷启动时长)"
- actual_RED_output: heartbeat_block_line=22507 bridge_init_line=22373 → FAIL: heartbeat 块在 bridge init 之后(窗口依赖 bridge 冷启动时长)
- actual_output: heartbeat_block_line=22407 bridge_init_line=22443 → PASS: heartbeat 先于 bridge init（harness at002 实测 delta=2s 辅助佐证）
- evidence_file: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-2.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 首版 wall-clock 时延断言在测试工位两次意外 PASS（冷启动下 delta=2s），根因是该工位 bridge init 耗时不同于生产（窗口长度=bridge 冷启动时长，环境相关）；改为确定性源码顺序断言：当前 heartbeat 块(~L22491)在 bridge init 块(~L22380)之后，必 FAIL。harness at002 时延实测保留为 GREEN 辅助证据

### acceptance-3
- id: AT-003
- requirement: heartbeat 判死动作走带验证的 teardown，不再裸 kill（C2a）
- acceptance_target: ensure_manager_once 的 heartbeat-stale 分支调用 restart_manager_supervisor_preserving_handoff 且含 kill -0 消亡验证；不含裸 `kill "$current_pid"`
- testing_layer: unit
- target_environment: fix/raw-20260717T004620Z-supervisor-liveness-storm
- required_evidence: 函数体源码断言输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-3.log
- test_command: |
  F=docs/system/workspace/scripts/runtime/freely
  BODY=$(awk '/^ensure_manager_once\(\)/,/^}/' "$F")
  if printf '%s' "$BODY" | grep -q 'kill "\$current_pid"'; then echo "FAIL: 仍有裸 kill"; \
  elif ! printf '%s' "$BODY" | grep -q 'restart_manager_supervisor_preserving_handoff'; then echo "FAIL: 未接入 teardown 通道"; \
  else echo "PASS: teardown 通道 + 无裸 kill"; fi
- expected_output: "PASS: teardown 通道 + 无裸 kill"
- expected_RED_output: "FAIL: 仍有裸 kill"
- actual_RED_output: FAIL: 仍有裸 kill（ensure_manager_once 含 kill "$current_pid"）
- actual_output: PASS: teardown 通道 + 无裸 kill
- evidence_file: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-3.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 当前源码 L19252 即裸 `kill "$current_pid"`，断言必 FAIL

### acceptance-4
- id: AT-004
- requirement: EXIT trap 不再互相覆盖，heartbeat 块之后 cleanup_supervisor 仍在 EXIT 链上（C1c）
- acceptance_target: supervisor 启动序列中 EXIT trap 为合并 handler（同时含 heartbeat 子进程回收与 cleanup_supervisor），不存在覆盖 cleanup_supervisor 的孤立 `trap 'kill $_heartbeat_bg_pid' EXIT`
- testing_layer: unit
- target_environment: fix/raw-20260717T004620Z-supervisor-liveness-storm
- required_evidence: trap 声明源码断言输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-4.log
- test_command: |
  F=docs/system/workspace/scripts/runtime/freely
  ISOLATED=$(grep -F "trap 'kill \$_heartbeat_bg_pid" "$F" | grep -vc "cleanup_supervisor" || true)
  MERGED=$(grep -cE "trap .*(_heartbeat_bg_pid).*(cleanup_supervisor)|trap .*(cleanup_supervisor).*(_heartbeat_bg_pid)|trap ._supervisor_exit_handler. EXIT" "$F" || true)
  if [ "$ISOLATED" -gt 0 ]; then echo "FAIL: 存在覆盖 cleanup_supervisor 的孤立 heartbeat EXIT trap"; \
  elif [ "$MERGED" -lt 1 ]; then echo "FAIL: 未找到合并 EXIT handler"; \
  else echo "PASS: EXIT trap 已合并"; fi
- expected_output: "PASS: EXIT trap 已合并"
- expected_RED_output: "FAIL: 存在覆盖 cleanup_supervisor 的孤立 heartbeat EXIT trap"
- actual_RED_output: FAIL: 存在覆盖 cleanup_supervisor 的孤立 heartbeat EXIT trap (isolated=1 merged=0)
- actual_output: PASS: EXIT trap 已合并 (isolated=0 merged=1)
- evidence_file: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-4.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 当前 L22340 的 cleanup trap 被 L22509 覆盖，grep 断言必 FAIL

### acceptance-5
- id: AT-005
- requirement: supervisor 死亡进入 storm window 并在阈值触发信号（C4a）
- acceptance_target: ensure-manager 侧存在死亡记录调用点；沙箱驱动阈值次数记录后 restart_storm_signal reason 非空
- testing_layer: integration
- target_environment: fix/raw-20260717T004620Z-supervisor-liveness-storm
- required_evidence: harness part-a/part-b 双 PASS
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-5.log
- test_command: bash docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/harness/at005-storm-window.sh
- expected_output: "AT-005 PASS"
- expected_RED_output: "part-a FAIL: record_supervisor_death_for_storm_window 函数不存在"
- actual_RED_output: part-a FAIL: record_supervisor_death_for_storm_window 函数不存在; part-b FAIL: 10 次记录后 storm reason 为空 → AT-005 FAIL
- actual_output: part-a PASS; part-b PASS: 阈值 10 次死亡记录后 storm reason='restart_storm_count_threshold' → AT-005 PASS
- evidence_file: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-5.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 当前不存在死亡记录函数，harness part-a 必 FAIL

### acceptance-6
- id: AT-006
- requirement: storm 阈值口径一致且可达（C4b）
- acceptance_target: PROCESS_CHURN_PEAK config 默认 ≤3（计数口径上限）；RESTART_STORM_COUNT 函数后备值 == config init 值
- testing_layer: unit
- target_environment: fix/raw-20260717T004620Z-supervisor-liveness-storm
- required_evidence: 数值提取比较输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-6.log
- test_command: |
  F=docs/system/workspace/scripts/runtime/freely
  PEAK=$(grep -oE 'PROCESS_CHURN_PEAK[ ]*=[ ]*[0-9]+' "$F" | head -1 | grep -oE '[0-9]+')
  CFG=$(grep -oE 'RESTART_STORM_COUNT[ ]*=[ ]*[0-9]+' "$F" | head -1 | grep -oE '[0-9]+')
  FB=$(grep -oE 'RESTART_STORM_COUNT:-[0-9]+' "$F" | head -1 | grep -oE '[0-9]+$')
  echo "peak=$PEAK cfg_count=$CFG fallback_count=$FB"
  if [ "${PEAK:-99}" -le 3 ] && [ -n "$CFG" ] && [ "$CFG" = "$FB" ]; then echo "PASS: 阈值口径一致且可达"; else echo "FAIL: peak=$PEAK cfg=$CFG fb=$FB"; fi
- expected_output: "PASS: 阈值口径一致且可达"
- expected_RED_output: "FAIL: peak=10 cfg=10 fb=4"
- actual_RED_output: peak=10 cfg_count=10 fallback_count=4 → FAIL: peak=10 cfg=10 fb=4
- actual_output: peak=3 cfg_count=10 fallback_count=10 → PASS: 阈值口径一致且可达
- evidence_file: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-6.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 当前 config init PROCESS_CHURN_PEAK=10（不可达）且 fallback 4≠config 10，断言必 FAIL

### acceptance-7
- id: AT-007
- requirement: 回归——stale heartbeat 前置下 auto 模式完整链走通（C1a 回归 + 全链）
- acceptance_target: L010→L020→L021→L022→L040 全部出现（≤240s）、0 次 daemon_signal_ignored、daemon-run ≤1
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T004620Z-supervisor-liveness-storm
- required_evidence: harness observed 行 + PASS 判定
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-7.log
- test_command: bash docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/harness/at007-auto-chain-e2e.sh
- expected_output: "AT-007 PASS: auto 模式全链走通且无误杀/双 daemon"
- expected_RED_output: "AT-007 FAIL: ignored>=1（复现 2026-07-17T00:33:31Z daemon_signal_ignored）"
- actual_RED_output: observed chain_complete=1 L040_within_240s=1 ignored_TERM=1 daemon_runs=2 → AT-007 FAIL: ignored=1 daemon_runs=2（链路能走通但复现误杀 TERM 与双 daemon）
- actual_output: observed: chain_complete=1 L040_within_240s=1 ignored_TERM=0 daemon_runs=1 → AT-007 PASS: auto 模式全链走通且无误杀/双 daemon
- evidence_file: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T004620Z/verification/test-evidence/acceptance-7.log
- red-green-status: green
- status: pass
- blocker:
- red_how: fix — 与 2026-07-17T00:33 生产复现同法：stale heartbeat + auto 启动，当前代码必出 daemon_signal_ignored

## Unit
- acceptance_target: ensure_manager_once kill 路径 / EXIT trap 声明 / 阈值口径 的源码级断言
- testing_layer: unit
- target_environment: fix/raw-20260717T004620Z-supervisor-liveness-storm
- required_evidence: AT-003 / AT-004 / AT-006 test_command 输出 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-003 teardown 通道断言
2. AT-004 EXIT trap 合并断言
3. AT-006 阈值口径断言

## Integration
- acceptance_target: heartbeat 启动时延实测 / storm window 沙箱行为
- testing_layer: integration
- target_environment: test-pre-merge-20260717T004620Z-supervisor-liveness-storm
- required_evidence: AT-002 / AT-005 harness PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-002 heartbeat 时延
2. AT-005 storm window 行为

## End-to-End
- acceptance_target: stale heartbeat 前置的真实 daemon 启动（wait 模式生存测试 + auto 模式全链回归）
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T004620Z-supervisor-liveness-storm → develop merge chain
- required_evidence: AT-001 / AT-007 harness PASS + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. AT-001 stale heartbeat 生存测试
2. AT-007 auto 全链回归

## Real-Environment
- real_environment_status: pass
- real_environment_reason: AT-001/AT-007 在 test-pre-merge-20260717T004620Z-supervisor-liveness-storm 以真实 daemon + 真实 AI CLI(claude-apikey-ds-flash-auto)执行通过：stale heartbeat 下单 supervisor 存活、auto 模式 L010→L040 全链、0 次误杀 TERM、单 daemon
