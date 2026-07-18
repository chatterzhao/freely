# Pre-Tests: runtime L2120 孤儿行 unbound 静默死修复
- issue_id: I-20260718T004314Z-A

RED 用主仓 develop 现行版脚本（含 L2120）；GREEN 用工位修复版。两条 harness 均以真实主仓 launch-state 为输入（触发条件天然满足）。

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: sourced probe 调 manager_worker_launch_state_refresh_for_status 正常返回，无 "source_project: unbound variable"
- acceptance_target: candidate AC1
- testing_layer: integration
- target_environment: test-pre-merge-20260718T004314Z-l2120-source-project-unbound
- required_evidence: RED=unbound reproduced；GREEN=probe survived
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260718T004314Z/verification/harness/at001-refresh-unbound.sh
- test_command: bash docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260718T004314Z/verification/harness/at001-refresh-unbound.sh <freely_script> <main_root>
- expected_output: AT001_RESULT: PASS
- expected_RED_output: probe 静默死（rc=1 无 PROBE_END；unbound 消息被 refresh 内调用点 >/dev/null 2>&1 吞掉——与生产静默死一致）→ AT001_RESULT: FAIL
- actual_RED_output: "probe died (rc=1) without unbound msg" → AT001_RESULT: FAIL（直调 reconcile 无重定向时实证 line 2120: source_project: unbound variable）
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260718T004314Z/verification/test-evidence/acceptance-1-RED.log
- red-green-status: red
- status: pending
- blocker:
- red_how: 对主仓 develop 现行版脚本跑 harness，refresh 到 L2120 即 shell 级 unbound 死亡（直调 reconcile 无重定向实证 line 2120: source_project: unbound variable；经 refresh 调用点重定向则表现为纯静默死）

### acceptance-2
- id: AT-002
- requirement: bash -n 通过；daemon status 穿过 L25325 无防护 refresh 调用点（post-reconcile 字段 intake_active_items 出现）
- acceptance_target: candidate AC2
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260718T004314Z-l2120-source-project-unbound
- required_evidence: RED=输出止于 reconcile 前；GREEN=post-reconcile 字段出现
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260718T004314Z/verification/harness/at002-daemon-start-past-reconcile.sh
- test_command: bash docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260718T004314Z/verification/harness/at002-daemon-start-past-reconcile.sh <freely_script> <main_root>
- expected_output: AT002_RESULT: PASS
- expected_RED_output: "output ends before post-reconcile fields" → AT002_RESULT: FAIL
- actual_RED_output: rc=1，输出止于 'control_plane: daemon'，post-reconcile 字段缺失 → AT002_RESULT: FAIL
- actual_output: (GREEN 阶段执行后填写)
- evidence_file: docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/raw-20260718T004314Z/verification/test-evidence/acceptance-2-RED.log
- red-green-status: red
- status: pending
- blocker:
- red_how: HEAD 版 daemon status 实测仅输出 control_plane 行即死（rc=1），intake_active_items（refresh 点之后打印）缺失即 RED

## Unit
- acceptance_target: N/A
- testing_layer: unit
- target_environment: N/A
- required_evidence: N/A
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: no_executable_boundary_at_this_layer
- not_applicable_explanation: 单行死代码删除，无独立单元面；bash -n 已并入 AT-002
- replacement_evidence: AT-001 函数级 probe + AT-002 语法/E2E

## Integration
- acceptance_target: refresh 函数级存活（AT-001）
- testing_layer: integration
- target_environment: test-pre-merge-20260718T004314Z-l2120-source-project-unbound
- required_evidence: AT001_RESULT: PASS
- blocker_taxonomy: execution_pending_or_failed
1. at001-refresh-unbound.sh — sourced probe 存活断言

## End-to-End
- acceptance_target: daemon status 全输出（AT-002）+ guarded merge chain
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260718T004314Z-l2120-source-project-unbound → develop merge chain
- required_evidence: AT002_RESULT: PASS + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. at002-daemon-start-past-reconcile.sh — post-reconcile 字段断言

## Real-Environment
- real_environment_status: pass
- real_environment_reason: harness 直接以真实主仓 launch-state（round-078 残留 prompts 现场）为输入，RED/GREEN 都在真实触发条件下执行；合并后 runtime 重启为最终 followthrough
