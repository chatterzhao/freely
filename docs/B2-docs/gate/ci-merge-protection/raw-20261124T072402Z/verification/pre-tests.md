# Pre-Tests: 更正 governance check 文档断言
- issue_id: I-20261124T072402Z-A

## Acceptance Items

### acceptance-1
- id: AT-001
- requirement: workflow 注释与实现一致，不再声称会置 check success
- acceptance_target: 文档修正 + 静态 AT
- testing_layer: integration
- target_environment: test-pre-merge-20261124T072402Z-governance-check-success-wiring
- required_evidence: AT 在 develop 基线 RED、工位 GREEN
- evidence_level: integration
- artifact_ref: docs/B2-docs/gate/ci-merge-protection/raw-20261124T072402Z/verification/test-evidence/acceptance-1.log
- test_command: python3 docs/system/workspace/scripts/tests/test-governance-check-doc-alignment.py
- expected_output: SUMMARY: N ok, 0 failed
- expected_RED_output: SUMMARY: <N-M> ok, M failed（基线注释仍含 "sets it to success" 且 AT 不存在/源断言不成立）
- actual_RED_output: "SUMMARY: 2 ok, 3 failed — 基线注释含误导性 sets it to success 声称、缺 in_progress 设计态说明、缺本地合并指向"
- actual_output: "SUMMARY: 5 ok, 0 failed"
- evidence_file: docs/B2-docs/gate/ci-merge-protection/raw-20261124T072402Z/verification/test-evidence/acceptance-1.log
- red-green-status: green
- status: passed
- red_how: fix 复现——develop 基线 workflow 注释第 3 条含误导性声称，AT 检测必然失败。

## Unit
- acceptance_target: workflow 注释文本断言
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: AT 静态断言部分
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 断言注释不含 `"sets it to success"` 误导性声称，含 in_progress 设计态说明。
  2. 断言 pr-merge-guarded 源码无 `_set_governance_check_pass(` 调用。

## Integration
- acceptance_target: AT 接入 test-all 且全绿
- testing_layer: integration
- target_environment: test-pre-merge-20261124T072402Z-governance-check-success-wiring
- required_evidence: `bash bin/test-all --ci` 全绿
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 执行 `bash bin/test-all --ci` 确认新 AT 被纳入且全绿。

## End-to-End
- acceptance_target: 分支保护启用态下合并链路不受影响
- testing_layer: end-to-end
- target_environment: develop（平台）
- required_evidence: `gh api branches/develop` protected=true 且 required check 正确；pr-merge-guarded 本地 merge+push 不查 check status
- blocker_taxonomy: execution_pending_or_failed
- test_tasks:
  1. 读取分支保护 API 确认 contexts 含 governance/pr-merge-guard。
  2. 源码确认 pr-merge-guarded 用本地 git merge + push，不查 check status。

## Real-Environment
- real_environment_status: pass
- real_environment_reason: 分支保护已在 develop 启用（protected=true），R60 已实证本地合并+push 在保护态下可用；本轮为文档修正，无运行时行为变化。
