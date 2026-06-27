# Pre-Tests: Agent 生命周期管理
- issue_id: I-20260627T084523Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: manager_reconcile 可被 sync_tooling 调用
- testing_layer: unit
- target_environment: fix/raw-20260627T084523Z-agent-lifecycle
- required_evidence: 函数返回 0
- test_command: source docs/system/workspace/scripts/runtime/freely && manager_reconcile_agent_id_env && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output:
- evidence_file:
- blocker:
- status: pending

### acceptance-2
- acceptance_target: --list worker 返回 10 个具体编号
- testing_layer: unit
- target_environment: fix/raw-20260627T084523Z-agent-lifecycle
- required_evidence: 输出含 worker_02
- test_command: ./bin/agent-table-query --list worker | grep -c "worker_" 
- expected_output: "10"
- actual_output:
- evidence_file:
- blocker:
- status: pending

### acceptance-3
- acceptance_target: wt-close 后 agent-id.env 无残留
- testing_layer: integration
- target_environment: test-pre-merge-20260627T084523Z-agent-lifecycle
- required_evidence: agent-id.env 不含该 raw-key
- test_command: grep -c "raw-20260627T084523Z" .freely/agent-id.env && echo "FAIL: zombie found" || echo "PASS: clean"
- expected_output: "PASS: clean"
- actual_output:
- evidence_file:
- blocker:
- status: pending

## Unit
- acceptance_target: 三个函数（reconcile, _acp_session_close, count_active）单元可用

## Integration
- acceptance_target: sync_tooling 分配不同 worker_NN（不总是 worker_01）

## End-to-End
- acceptance_target: freely daemon 启动后 agent-id.env 无僵尸条目，并发控制生效

## Real-Environment
- real_environment_status: not_tested
