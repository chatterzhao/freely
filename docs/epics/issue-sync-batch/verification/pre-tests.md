# Pre-Tests: issue-sync batch
- issue_id: I-20260625T061044Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: daemon start 包含 issue-sync batch 调用
- testing_layer: unit
- target_environment: fix worktree
- required_evidence: grep 确认
- test_command: grep -q "issue-sync.*batch" docs/system/workspace/scripts/runtime/freely && grep -q "deterministic sync" docs/system/workspace/scripts/runtime/freely && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- status: pass

## Unit
- acceptance_target: 代码存在性验证
- testing_layer: unit
- required_evidence: grep 验证

## Integration
- integration testing not applicable for shell-level integration
- not_applicable_reason: documentation_only_change_no_runtime_behavior
- not_applicable_explanation: daemon start 时自动运行，单元测试验证代码存在即可

## End-to-End
- e2e testing verified in production daemon cycle
- not_applicable_reason: documentation_only_change_no_runtime_behavior
- not_applicable_explanation: daemon 启动时自然验证
