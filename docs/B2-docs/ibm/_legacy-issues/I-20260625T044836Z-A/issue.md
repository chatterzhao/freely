- issue_id: I-20260625T044836Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260625T044836Z-A
- source_candidate: docs/pre-brainstorms/20260625T044836Z--issue-sync-filter/candidates.md#C-20260625T044836Z-A
- verification_artifact_dir: docs/epics/issue-sync-filter/code-reviews
- canonical_issue_path: docs/issues/I-20260625T044836Z-A/issue.md
- source_raw: raw-20260625T044836Z
- pre_tests_path: docs/epics/issue-sync-filter/verification/pre-tests.md
- title: issue-sync filter skip closed issues

# I-20260625T044836Z-A: issue-sync filter

- source_candidate: docs/pre-brainstorms/20260625T044836Z--issue-sync-filter/candidates.md#C-20260625T044836Z-A
- verification_artifact_dir: docs/epics/issue-sync-filter/code-reviews
- pre_tests_path: docs/epics/issue-sync-filter/verification/pre-tests.md

## 实现
- cmd_batch: 收集时跳过 platform_state=closed 的 issue
- 输出: 显示 skipped count
