- issue_id: I-20260624T151020Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260624T151020Z-A
- source_candidate: docs/B1-docs/raw-20260624T151020Z20Z/candidates.md#C-20260624T151020Z-A
- verification_artifact_dir: docs/B2-docs/wt-close-gate-args/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260624T151020Z-A/issue.md
- title: wt-close pretests-retirement-gate 传参修复

# I-20260624T151020Z-A: wt-close pretests-retirement-gate 传参修复

- source_candidate: docs/B1-docs/raw-20260624T151020Z20Z/candidates.md#C-20260624T151020Z-A
- source_raw: raw-20260624T151020Z20Z
- verification_artifact_dir: docs/B2-docs/wt-close-gate-args/code-reviews

## 实现

仅修改 docs/system/workspace/scripts/worktree/wt-close 第 322 行，
将 pretests-retirement-gate 调用从裸位置参数改为 --project + --worktree-path 标志。
