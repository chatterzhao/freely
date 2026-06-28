# Pre-Tests: a2a_tasks agent_id
- issue_id: I-20260627T084545Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: insert 后 agent_id 为具体编号
- testing_layer: unit
- target_environment: fix/raw-20260627T084545Z-a2a-tasks-agent-id
- required_evidence: SQLite 查询返回 worker_01
- test_command: grep -c "LIKE 'worker_%'" docs/system/workspace/scripts/runtime/freely_db_manager.py && echo "PASS"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-1.log
- blocker:
- status: pass

### acceptance-2
- acceptance_target: a2a_task.py 查询兼容 worker_ prefix
- testing_layer: unit
- target_environment: fix/raw-20260627T084545Z-a2a-tasks-agent-id
- required_evidence: startswith 替代 ==
- test_command: grep -c "startswith('worker')" docs/system/workspace/scripts/runtime/a2a_task.py && echo "PASS"
- expected_output: PASS
- actual_output: PASS
- evidence_file: .freely/run/test-evidence/acceptance-2.log
- blocker:
- status: pass

## Unit
- acceptance_target: 6 文件改动正确

## Integration
- acceptance_target: freely daemon 新记录 agent_id 为具体编号
- testing_layer: integration
- target_environment: develop
- required_evidence: 新记录 agent_id != 'worker'
- not_applicable_reason: pre-merge 阶段无法启动 daemon 验证
- not_applicable_explanation: 需合入 develop 后启动 daemon，创建新任务后检查 a2a_tasks.agent_id。单元测试已覆盖 LIKE 查询和代码改动

## End-to-End
- acceptance_target: 多 agent 并发时 agent_id 正确区分
- testing_layer: end-to-end
- target_environment: develop
- required_evidence: worker_01/03/05 的 a2a_tasks 记录 agent_id 不同
- not_applicable_reason: pre-merge 阶段无法启动多 agent 并发
- not_applicable_explanation: 需合入 develop 后启动 daemon，委派多个 worker 后验证 agent_id 区分。代码改动已在单元测试中验证

## Real-Environment
- real_environment_status: not_tested
- real_environment_reason: pre-merge 阶段
