# Pre-Tests: liveness 兜底链修复
- issue_id: I-20260716T114802Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: niced 存活进程判活（AC1）
- acceptance_target: S1 过期、socket 不存在、无 worker 时，真实 nice 进程（态 SN）仅凭 S2 判活
- testing_layer: integration
- target_environment: fix/raw-20260716T114802Z-return-value-fix
- required_evidence: harness 输出 PASS + 实测进程态
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/verification/test-evidence/acceptance-1.log
- test_command: bash docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/verification/harness/at001-niced-liveness.sh
- expected_output: "AT-001 PASS: niced 存活进程(state=SN)判活"
- expected_RED_output: "AT-001 FAIL: niced 存活进程(state=SN)被判死(S2 精确匹配击穿)"
- actual_RED_output: AT-001 FAIL: niced 存活进程(state=SN)被判死(S2 精确匹配击穿)
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/verification/test-evidence/acceptance-1.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — 真实 nice -n 10 进程 ps 态为 SN，当前精确匹配 R/S 必判死（06:11:47 生产误杀同路径）

### acceptance-2
- id: AT-002
- requirement: 源码断言（AC2）
- acceptance_target: S2 为前缀匹配 R*/S*；函数内存在 base_tool 安全推导
- testing_layer: unit
- target_environment: fix/raw-20260716T114802Z-return-value-fix
- required_evidence: 断言输出
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/verification/test-evidence/acceptance-2.log
- test_command: |
  BODY=$(awk '/^_ai_shows_liveness_acp\(\)/,/^}/' docs/system/workspace/scripts/runtime/freely)
  P2=0; printf '%s' "$BODY" | grep -q 'proc_state" == R\* || "$proc_state" == S\*' && P2=1
  P3=0; printf '%s' "$BODY" | grep -q 'local base_tool=' && P3=1
  echo "prefix_match=$P2 base_tool_derived=$P3"
  if [ "$P2" -eq 1 ] && [ "$P3" -eq 1 ]; then echo "PASS: S2/S3 修复在位"; else echo "FAIL: prefix=$P2 basetool=$P3"; fi
- expected_output: "PASS: S2/S3 修复在位"
- expected_RED_output: "FAIL: prefix=0 basetool=0"
- actual_RED_output: prefix_match=0 base_tool_derived=0 → FAIL: prefix=0 basetool=0
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/verification/test-evidence/acceptance-2.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — 当前为精确匹配且无 local base_tool，断言必 FAIL

### acceptance-3
- id: AT-003
- requirement: set -u 下无 unbound（AC3）
- acceptance_target: base_tool 未定义环境下函数执行无 unbound variable 报错
- testing_layer: integration
- target_environment: fix/raw-20260716T114802Z-return-value-fix
- required_evidence: harness 输出 PASS
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/verification/test-evidence/acceptance-3.log
- test_command: bash docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/verification/harness/at003-setu-basetool.sh
- expected_output: "AT-003 PASS: 无 unbound variable"
- expected_RED_output: "AT-003 FAIL: base_tool unbound variable"
- actual_RED_output: AT-003 FAIL: base_tool unbound variable (1 处)
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/verification/test-evidence/acceptance-3.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — L13928 引用未定义 $base_tool，set -u 沙箱必报 unbound

### acceptance-4
- id: AT-004
- requirement: E2E 回归（AC4）
- acceptance_target: 真实 auto 启动 150s 窗口，AI 存活期间 0 次 runtime_stalled_ai_recovery_triggered
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260716T114802Z-return-value-fix
- required_evidence: harness observed 行 + PASS
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/verification/test-evidence/acceptance-4.log
- test_command: bash docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/verification/harness/at004-auto-no-stall-e2e.sh
- expected_output: "AT-004 PASS: 150s 窗口无 stall 误触发"
- expected_RED_output: "AT-004 FAIL 或 PASS（本项为回归防护——误杀依赖 debug 静默>90s 的时序，RED 阶段不强求复现，机制性 RED 由 AT-001/003 承担）"
- actual_RED_output: 生产实证 2026-07-16T13:11:47Z runtime_stalled_ai_recovery_triggered 误杀活跃 manager(reason=manager_ai_stalled_without_runtime_progress);时序依赖不做确定性 E2E 复现,机制 RED 由 AT-001/003 承担
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/raw-20260716T114802Z/verification/test-evidence/acceptance-4.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — 06:11:47 生产事件即该路径实证；时序依赖（debug 静默≥90s + 检查窗对齐）使 E2E 确定性复现不可行，机制性复现由 AT-001（真实 SN 进程判死）与 AT-003（unbound 实证）承担，本项承担修复后回归防护

## Unit
- acceptance_target: 源码断言
- testing_layer: unit
- target_environment: fix/raw-20260716T114802Z-return-value-fix
- required_evidence: AT-002 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-002

## Integration
- acceptance_target: 真实 niced 进程行为 + set -u 沙箱
- testing_layer: integration
- target_environment: fix/raw-20260716T114802Z-return-value-fix
- required_evidence: AT-001 / AT-003 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-001
2. AT-003

## End-to-End
- acceptance_target: 真实 auto 周期无 stall 误触发
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260716T114802Z-return-value-fix → develop merge chain
- required_evidence: AT-004 PASS + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. AT-004

## Real-Environment
- real_environment_status: fail
- real_environment_reason: pending — GREEN 阶段执行 AT-004 后更新
