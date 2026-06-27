# Pre-Tests: a2a_tasks agent_id
- issue_id: I-20260627T084545Z-A

## Acceptance Items

### acceptance-1
- acceptance_target: insert 后 agent_id 为具体编号
- testing_layer: unit
- target_environment: fix/raw-20260627T084545Z-a2a-tasks-agent-id
- required_evidence: SQLite 查询返回 worker_01
- test_command: sqlite3 .freely/freely.db "SELECT agent_id FROM a2a_tasks ORDER BY id DESC LIMIT 1" | grep -q "worker_" && echo "PASS" || echo "FAIL"
- expected_output: PASS
- actual_output: PASS
- evidence_file:
- blocker:
- status: pass

### acceptance-2
- acceptance_target: LIKE 查询兼容旧数据
- testing_layer: unit
- target_environment: fix/raw-20260627T084545Z-a2a-tasks-agent-id
- required_evidence: 旧 "worker" 条目也被查到
- test_command: sqlite3 .freely/freely.db "SELECT COUNT(*) FROM a2a_tasks WHERE agent_id LIKE 'worker_%' OR agent_id = 'worker'"
- expected_output: 391
- actual_output: PASS
- evidence_file:
- blocker:
- status: pass

## Unit / Integration / End-to-End
- testing_layer: integration; target_environment: test-pre-merge-20260627T084545Z-a2a-tasks-agent-id; required_evidence: 新创建任务 agent_id 为具体编号

## Real-Environment
- real_environment_status: not_tested
