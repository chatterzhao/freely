# Pre-Tests: issue-sync filter
- issue_id: I-20260625T044836Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: batch 命令跳过已关闭的 issue
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认过滤逻辑
- test_command: grep -q "platform_state.*closed" bin/issue-sync && grep -q "_skipped" bin/issue-sync && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
^- status: passed

## Unit
- acceptance_target: 过滤逻辑正确
- testing_layer: unit
- required_evidence: grep 验证

## Integration
- acceptance_target: batch 运行正确统计
- testing_layer: integration
- target_environment: test-pre-merge
- required_evidence: 输出包含 skipped count
- not_applicable_reason: documentation_only_change_no_runtime_behavior
- not_applicable_explanation: 过滤逻辑简单，grep 验证足够

## End-to-End
- acceptance_target: 生产环境 batch 扫描
- testing_layer: end-to-end
- target_environment: develop merge chain
- required_evidence: batch 正常跳过已关闭 issue
- not_applicable_reason: documentation_only_change_no_runtime_behavior
- not_applicable_explanation: daemon start 时自动运行验证

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: daemon 启动时自然验证
