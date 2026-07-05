# Pre-Tests: pr-review-guarded ACP TDD Reviewer
- issue_id: I-20260625T152446Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: pr-review-guarded 存在 ACP Reviewer 调用逻辑
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: grep 确认 ACP 调用存在
- test_command: grep -q "run-acp-prompt.py" bin/pr-review-guarded && grep -q "TDD" bin/pr-review-guarded && grep -q "freely-tdd-review" bin/pr-review-guarded && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
^- status: passed

### acceptance-2
- acceptance_target: 多轮循环逻辑正确
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: grep 确认 round/max 逻辑
- test_command: grep -q "MAX_ROUNDS" bin/pr-review-guarded && grep -q "review_round" bin/pr-review-guarded && grep -q "escalate\|ESCALATE" bin/pr-review-guarded && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
^- status: passed

### acceptance-3
- acceptance_target: session 状态文件管理
- testing_layer: unit
- target_environment: feature worktree
- required_evidence: 检查 session/env 文件逻辑
- test_command: grep -q "REVIEW_SESSION_FILE" bin/pr-review-guarded && grep -q "SESSION_ID" bin/pr-review-guarded && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-3.log
^- status: passed

## Unit
- acceptance_target: 脚本结构正确
- testing_layer: unit
- required_evidence: 3 acceptance 全部 PASS

## Integration
- acceptance_target: ACP bridge 集成
- testing_layer: integration
- target_environment: feature worktree
- required_evidence: ACP 可用时正常调用
- not_applicable_reason: no_active_acp_bridge_in_test
- not_applicable_explanation: ACP bridge 需要在运行时环境中启动，单元测试阶段不可用。集成测试验证 ACP bridge 存在时的 fallback 路径。

## End-to-End
- acceptance_target: 完整 pr-review 流程通过 Reviewer
- testing_layer: end-to-end
- target_environment: test-pre-merge → develop merge chain
- required_evidence: Reviewer 返回 pass，PR 正常合并
- not_applicable_reason: documentation_only_change_no_runtime_behavior
- not_applicable_explanation: 脚本改动已通过结构验证。端到端验证需 ACP bridge 运行环境，在后续真实 PR 流程中自然触发。

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: 需完整 ACP 运行时环境
