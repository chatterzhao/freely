# Pre-Tests: session restore 退出码
- issue_id: I-20261124T054241Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: 恢复失败时非零退出 + 结构化汇总
- acceptance_target: agent_session_restore.main() 退出码与输出
- testing_layer: integration
- target_environment: test-pre-merge-20261124T054241Z-session-restore-exit-code
- required_evidence: AT 在 develop 基线 RED、工位 GREEN
- evidence_level: integration
- artifact_ref: docs/B2-docs/runtime/daemon/raw-20261124T054241Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-session-restore-exit-code.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: <N-M> ok, M failed（基线 failed outcome 仍返回 0、无汇总）
- actual_RED_output: "SUMMARY: 4 ok, 2 failed — 基线 failed outcome 仍返回 0、无 health 汇总"
- actual_output: "SUMMARY: 6 ok, 0 failed；failed→非零、全 resumed→0、usage→2 均验证"
- evidence_file: docs/B2-docs/runtime/daemon/raw-20261124T054241Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix 复现——develop 基线 main() 对 failed outcome 恒返回 0，AT mock 行为断言必然失败。

## Unit
- acceptance_target: main() 退出码与汇总逻辑
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: mock outcomes 后 main() 返回值断言
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. mock failed outcome → main(["proj"]) 返回非 0。
  2. mock 全 resumed → 返回 0；mock usage 错误 → 返回 2（不变）。
  3. 输出含 resumed/failed/slot_unavailable 计数与 health 汇总。

## Integration
- acceptance_target: 与 test-all 回归兼容
- testing_layer: integration
- target_environment: test-pre-merge-20261124T054241Z-session-restore-exit-code
- required_evidence: `bash bin/test-all --ci` 全绿
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 新 AT 接入 CORE/CI_CORE 并跑 test-all --ci 全绿。

## End-to-End
- acceptance_target: 恢复链路语义不变
- testing_layer: end-to-end
- target_environment: test-pre-merge → develop merge chain
- required_evidence: guarded merge receipts + 逐条 outcome 打印格式不变
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. AT 断言逐条 outcome JSON 行仍原样打印（返回结构不变）。
  2. 合并后 runtime 不因新退出码产生回归（test-all 覆盖）。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 本轮改的是 CLI 退出码契约，fix/test 工位以 mock outcomes 真机调用 main() 即为真实环境验证；不触发真实 session/resume。
