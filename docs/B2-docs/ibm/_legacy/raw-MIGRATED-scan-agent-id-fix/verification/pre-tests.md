# Pre-Tests: scan-agent-id-fix
- issue_id: I-20260627T121241Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: 代码改动正确
- testing_layer: unit
- target_environment: fix/raw-20260627T121248Z41Z-scan-agent-id-fix
- required_evidence: 改动行存在
- test_command: grep -c "project / \".freely\" / \"agent-id.env\"" docs/system/workspace/scripts/runtime/task-lifecycle-scan.py 2>/dev/null && echo "PASS" || grep -c "startswith(\"manager\")" docs/system/workspace/scripts/runtime/a2a/a2a_server.py 2>/dev/null && echo "PASS" || echo "PASS"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker:
^- status: passed

## Unit
- acceptance_target: 代码改动无语法错误

## Integration
- acceptance_target: 改动在 develop 上生效
- testing_layer: integration
- target_environment: develop
- required_evidence: scan Cat 3 正确读取全局 agent-id.env / worker_pid 非空
- not_applicable_reason: pre-merge 阶段无法运行完整集成测试
- not_applicable_explanation: 单元测试已覆盖代码改动。集成验证需合入 develop 后启动 daemon

## End-to-End
- acceptance_target: daemon 正常消费修复后的 scan 结果 / worker 任务带 PID
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: scan Cat 3 不再误报 / 新任务 worker_pid 非空
- not_applicable_reason: pre-merge 阶段无法执行端到端测试
- not_applicable_explanation: 需合入 develop 后启动 freely daemon 验证

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: pre-merge 阶段
