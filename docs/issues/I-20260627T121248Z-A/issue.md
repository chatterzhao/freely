- issue_id: I-20260627T121248Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260627T121248Z-A
- source_candidate: docs/pre-brainstorms/20260627T121248Z--a2a-worker-pid-fix/candidates.md#C-20260627T121248Z-A
- source_raw: raw-20260627T121248Z
- verification_artifact_dir: docs/epics/a2a-worker-pid-fix/code-reviews
- canonical_issue_path: docs/issues/I-20260627T121248Z-A/issue.md
- title: a2a worker_pid + manager check 修复

# I-20260627T121248Z-A: a2a worker_pid + manager check

- source_candidate: docs/pre-brainstorms/20260627T121248Z--a2a-worker-pid-fix/candidates.md#C-20260627T121248Z-A

## 实现
- freely: insert 时传 --worker-pid
- a2a_server.py: agent_id == "manager" → startswith("manager")
