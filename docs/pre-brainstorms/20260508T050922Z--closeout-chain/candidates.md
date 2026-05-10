# Candidates

## C-20260508T050922Z-A: 门禁收口链路修复

- candidate_format_version: v2
- title: issue-sync close 支持从 raw-* 继承 platform_ids
- status: promoted
- promoted_issue_path: docs/issues/I-20260508T050922Z-A/issue.md
- milestone: M-20260508T050922Z-A
- next_action: B2_IBM → dev-loop → merge
- acceptance_criteria:
  - I-* issue 无 platform_ids 时可追溯 raw-* parent 关闭
  - issue-sync promote 正确写入 platform_ids
