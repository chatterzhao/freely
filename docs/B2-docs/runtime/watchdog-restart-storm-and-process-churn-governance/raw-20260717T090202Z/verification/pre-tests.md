# Pre-Tests: peak 口径修正
- issue_id: I-20260717T090202Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: cycle 不触发/death 触发/口径文档化（AC1/AC3）
- acceptance_target: 沙箱 5 次 cycle 记录 reason=none；3 次 death 记录 reason=process_churn_peak_threshold；capability-lifecycle 有口径说明
- testing_layer: integration
- target_environment: fix/raw-20260717T090202Z-peak-misfire-regression
- required_evidence: harness observed 行 + PASS
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T090202Z/verification/test-evidence/acceptance-1.log
- test_command: bash docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T090202Z/verification/harness/at001-peak-kind.sh
- expected_output: "AT-001 PASS: cycle 不触发/death 触发/口径已文档化"
- expected_RED_output: "AT-001 FAIL: cycle=process_churn_peak_threshold（健康 cycle 行即触发）"
- actual_RED_output: observed: cycle_reason=process_churn_peak_threshold death_reason=process_churn_peak_threshold doc=0 → AT-001 FAIL（健康 cycle 行即触发;生产 08:59:43Z 实证）
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T090202Z/verification/test-evidence/acceptance-1.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — 现状 peak 统计全部行,5 次 cycle 记录(count=3)即触发,生产 08:59:43Z 起每 cycle 实抓

### acceptance-2
- id: AT-002
- requirement: E2E 零误 pause（AC2）
- acceptance_target: 真实 daemon wait 90s 观察窗 0 次 restart_storm_pause
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T090202Z-peak-misfire-regression
- required_evidence: harness observed 行 + PASS
- evidence_level: real_env
- artifact_ref: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T090202Z/verification/test-evidence/acceptance-2.log
- test_command: bash docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T090202Z/verification/harness/at002-no-false-pause.sh
- expected_output: "AT-002 PASS: 零误 pause"
- expected_RED_output: "AT-002 FAIL: pauses>=1"
- actual_RED_output: 等待 auto 短窗 RED（生产每 cycle 一次 pause 已实证）
- actual_output: (GREEN 后填写)
- evidence_file: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T090202Z/verification/test-evidence/acceptance-2.log
- red-green-status: red
- status: pending
- blocker:
- red_how: fix — wait 模式无 AI cycle,storm window 记录来自…（wait 模式下 update 调用点=AI cycle 完成,wait 不产生记录→RED 需 auto 短窗或注入记录;取 auto 60s 短窗:每 cycle 后必 pause,生产已实抓）

## Unit
- acceptance_target: 无独立单元面
- testing_layer: unit
- target_environment: fix/raw-20260717T090202Z-peak-misfire-regression
- required_evidence: n/a
- blocker_taxonomy: execution_pending_or_failed
- not_applicable_reason: covered_by_more_realistic_required_surface
- not_applicable_explanation: 口径为 awk/函数行为,AT-001 沙箱即最小行为面
- replacement_evidence: AT-001 observed

## Integration
- acceptance_target: 沙箱 cycle/death 矩阵
- testing_layer: integration
- target_environment: fix/raw-20260717T090202Z-peak-misfire-regression
- required_evidence: AT-001 PASS
- blocker_taxonomy: execution_pending_or_failed
1. AT-001

## End-to-End
- acceptance_target: 真实 daemon 零误 pause
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260717T090202Z-peak-misfire-regression → develop merge chain
- required_evidence: AT-002 PASS + guarded merge receipts
- blocker_taxonomy: execution_pending_or_failed
1. AT-002

## Real-Environment
- real_environment_status: fail
- real_environment_reason: pending — GREEN 阶段执行 AT-002 后更新
