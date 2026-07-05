- issue_id: I-20260626T133842Z-A
- kind: fix
- phase_state: completed
- source_candidate: docs/pre-brainstorms/20260626T133842Z--feedback-exit-on-error/candidates.md#C-20260626T133842Z-A
- source_raw: raw-20260626T133842Z
- canonical_issue_path: docs/issues/I-20260626T133842Z-A/issue.md
- pre_tests_path: docs/epics/feedback-exit-on-error/verification/pre-tests.md
- title: freely feedback exits 1 on any platform creation failure

# I-20260626T133842Z-A: feedback exit on platform error

## 实现
- 去掉 || true，adapter 错误不再被吞
- 任一平台失败 → exit 1
- 全平台失败 → exit 1
