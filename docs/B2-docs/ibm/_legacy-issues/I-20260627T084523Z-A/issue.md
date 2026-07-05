- issue_id: I-20260627T084523Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260627T084523Z-A
- source_candidate: docs/B1-docs/raw-20260627T084545Z23Z/candidates.md#C-20260627T084523Z-A
- source_raw: raw-20260627T084545Z23Z
- verification_artifact_dir: docs/B2-docs/agent-lifecycle/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260627T084523Z-A/issue.md
- pre_tests_path: docs/B2-docs/agent-lifecycle/verification/pre-tests.md
- title: Agent 生命周期管理 — 僵尸清理、并发控制、session 关闭

# I-20260627T084523Z-A: Agent 生命周期管理

- source_candidate: docs/B1-docs/raw-20260627T084545Z23Z/candidates.md#C-20260627T084523Z-A
- verification_artifact_dir: docs/B2-docs/agent-lifecycle/code-reviews
- pre_tests_path: docs/B2-docs/agent-lifecycle/verification/pre-tests.md

## 实现
- Bug A: sync_tooling 写入前调 reconcile 清僵尸
- Bug B: 遍历 --list worker 选空闲，非 head -1
- Bug C: sync_tooling 入口加 reconcile + count 并发检查
- Bug D: 靠 A 覆盖（reconcile 自动清）
- Bug E: wt-close Phase 4.5 调 _acp_session_close
