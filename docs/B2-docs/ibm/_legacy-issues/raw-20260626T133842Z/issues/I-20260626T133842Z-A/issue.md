- issue_id: I-20260626T133842Z-A
- kind: fix
- phase_state: completed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260626T133842Z/code-reviews
- source_candidate: docs/B1-docs/raw-20260626T133842Z42Z/candidates.md#C-20260626T133842Z-A
- source_raw: raw-20260626T133842Z42Z
- canonical_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260626T133842ZI-20260626T133842Z-A/issue.md
- pre_tests_path: docs/B2-docs/feedback-exit-on-error/verification/pre-tests.md
- title: freely feedback exits 1 on any platform creation failure

# I-20260626T133842Z-A: feedback exit on platform error

## 实现
- 去掉 || true，adapter 错误不再被吞
- 任一平台失败 → exit 1
- 全平台失败 → exit 1
