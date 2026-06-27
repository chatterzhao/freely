- issue_id: I-20260627T084545Z-A
- kind: fix
- phase_state: done_b2_ibm
- milestone: M-20260627T084545Z-A
- source_candidate: docs/pre-brainstorms/20260627T084545Z--a2a-tasks-agent-id/candidates.md#C-20260627T084545Z-A
- source_raw: raw-20260627T084545Z
- verification_artifact_dir: docs/epics/a2a-tasks-agent-id/code-reviews
- canonical_issue_path: docs/issues/I-20260627T084545Z-A/issue.md
- pre_tests_path: docs/epics/a2a-tasks-agent-id/verification/pre-tests.md
- title: a2a_tasks agent_id 改具体编号 + 字段补全

# I-20260627T084545Z-A: a2a_tasks agent_id 改具体编号

- source_candidate: docs/pre-brainstorms/20260627T084545Z--a2a-tasks-agent-id/candidates.md#C-20260627T084545Z-A
- verification_artifact_dir: docs/epics/a2a-tasks-agent-id/code-reviews

## 实现
- freely:13601: --role worker → --role $_next_worker
- a2a_task.py:607: 不改（agent_id=role 本身正确）
- 6处 =='worker' 改为 LIKE 'worker_%'
- worker_pid 写入 + delivery_status 更新
