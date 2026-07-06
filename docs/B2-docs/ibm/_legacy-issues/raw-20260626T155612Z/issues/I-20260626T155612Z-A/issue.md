- issue_id: I-20260626T155612Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260626T155612Z-A
- source_raw: raw-20260626T155612Z12Z
- source_candidate: docs/B1-docs/raw-20260626T155612Z12Z/candidates.md#C-20260626T155612Z-A
- verification_artifact_dir: docs/B2-docs/issue-sync-before-merge/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260626T155612ZI-20260626T155612Z-A/issue.md
- title: pr-merge-guarded issue-sync before merge + auto-commit
- pre_tests_path: docs/B2-docs/issue-sync-before-merge/verification/pre-tests.md

# I-20260626T155612Z-A: pr-merge-guarded issue-sync before merge + auto-commit

- source_raw: raw-20260626T155612Z12Z
- source_candidate: docs/B1-docs/raw-20260626T155612Z12Z/candidates.md#C-20260626T155612Z-A
- pre_tests_path: docs/B2-docs/issue-sync-before-merge/verification/pre-tests.md
- verification_artifact_dir: docs/B2-docs/issue-sync-before-merge/code-reviews

## 实现

### 修改文件
- docs/system/workspace/scripts/worktree/pr-merge-guarded:
  _sync_issues_changed_in_merge 移到 merge 之前执行，
  新增 _target 参数，diff 改为 source vs target 比较，
  自动 commit + push 保持 source worktree 干净
