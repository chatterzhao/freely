# Pre-Tests: pr-create merge + checkpoint scope
- issue_id: I-20260627T135126Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: pr-create-guarded 使用 merge 策略
- testing_layer: unit
- target_environment: fix/raw-20260627T135126Z-checkpoint-merge-fix
- required_evidence: 代码不含 --rebase
- test_command: grep -L "pull --rebase" docs/system/workspace/scripts/worktree/pr-create-guarded && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker:
^- status: passed

### acceptance-2
- acceptance_target: checkpoint-guard merge 时跳过 scope
- testing_layer: unit
- target_environment: fix/raw-20260627T135126Z-checkpoint-merge-fix
- required_evidence: _is_merge_commit 函数存在
- test_command: grep -c "_is_merge_commit" docs/system/workspace/scripts/quality/checkpoint-guard && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker:
^- status: passed

## Unit
- acceptance_target: 两处改动语法正确，逻辑正确

## Integration
- acceptance_target: git merge develop 不再被 checkpoint 拦截
- testing_layer: integration
- target_environment: develop
- required_evidence: merge 成功
- not_applicable_reason: pre-merge 阶段无法直接 merge develop 验证
- not_applicable_explanation: 需合入 develop 后在实际工位中测试 git merge develop

## End-to-End
- acceptance_target: pr-create 流程不再被 scope 检查误拦
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: 多工位并行时 pr-create 顺利通过
- not_applicable_reason: pre-merge 阶段无法执行端到端测试
- not_applicable_explanation: 需合入 develop 后在真实多工位场景验证

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: pre-merge 阶段
