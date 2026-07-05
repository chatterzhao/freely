- issue_id: I-20260625T061044Z-A
- kind: fix
- phase_state: completed
- milestone: M-20260625T061044Z-A
- source_candidate: docs/B1-docs/raw-20260625T061044Z44Z/candidates.md#C-20260625T061044Z-A
- verification_artifact_dir: docs/B2-docs/issue-sync-batch/code-reviews
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/I-20260625T061044Z-A/issue.md
- source_raw: raw-20260625T061044Z44Z
- pre_tests_path: docs/B2-docs/issue-sync-batch/verification/pre-tests.md
- title: issue-sync batch before daemon scan

# I-20260625T061044Z-A: issue-sync batch

- source_candidate: docs/B1-docs/raw-20260625T061044Z44Z/candidates.md#C-20260625T061044Z-A
- verification_artifact_dir: docs/B2-docs/issue-sync-batch/code-reviews
- pre_tests_path: docs/B2-docs/issue-sync-batch/verification/pre-tests.md

## 实现
- cmd_daemon_start: platform 检测后 scan 前运行 issue-sync batch
- 输出: 记录到 daemon log
