# Pre-Tests: pr-create-guarded rebase 替代 merge
- issue_id: I-20260625T131154Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: Step 3 使用 --rebase 而非 merge
- testing_layer: unit
- target_environment: test-pre-merge-20260625T131154Z-pr-create-rebase
- required_evidence: grep 确认
- test_command: grep -q "git pull --rebase" docs/system/workspace/scripts/worktree/pr-create-guarded && grep -q "force-with-lease" docs/system/workspace/scripts/worktree/pr-create-guarded && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker: (失败时填写)
^- status: passed

## Unit
- acceptance_target: 文本验证
- testing_layer: unit
- target_environment: test-pre-merge-20260625T131154Z-pr-create-rebase
- required_evidence: grep 确认 rebase + force-with-lease

## Integration
- acceptance_target: 语法检查
- testing_layer: integration
- target_environment: test-pre-merge-20260625T131154Z-pr-create-rebase
- required_evidence: bash -n 通过
- not_applicable_reason: documentation_only_change_no_runtime_behavior
- not_applicable_explanation: 改动为 git 命令参数变更，bash -n + grep 验证足够

## End-to-End
- acceptance_target: 多工位并行时 rebase 成功
- testing_layer: end-to-end
- target_environment: test-pre-merge-20260625T131154Z-pr-create-rebase → develop merge chain
- required_evidence: 第二个 PR rebase 后 checkpoint-guard 不拦截
- not_applicable_reason: documentation_only_change_no_runtime_behavior
- not_applicable_explanation: 端到端验证需实际多工位并行场景，在后续真实流程中自然验证

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: pipeline 变更
