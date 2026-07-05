# Candidates

## C-20260508T050922Z-A: legacy issue

- candidate_format_version: v2
- title: issue-sync close 支持从 raw-* 继承 platform_ids
- status: promoted
- decision_reason: I-* close 链路断裂导致平台 issue 无法自动关闭，需要 raw-* 追溯继承 platform_ids
- promoted_issue_path: docs/issues/I-20260508T050922Z-A/issue.md
- milestone: M-20260508T050922Z-A
- completion_note: I-20260508T050922Z-A 已完成 closeout，close 链路修复已吸收到 develop
- next_action: B2_IBM → dev-loop → merge
- acceptance_criteria:
  - I-* issue 无 platform_ids 时可追溯 raw-* parent 关闭
  - issue-sync promote 正确写入 platform_ids
