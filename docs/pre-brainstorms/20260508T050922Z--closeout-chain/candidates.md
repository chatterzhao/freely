# Candidates

## C-20260508T050922Z-A: 门禁收口链路修复

- candidate_format_version: v2
- title: issue-sync close 支持从 raw-* 继承 platform_ids
- status: promoted
- decision_reason: I-* close 链路断裂导致平台 issue 无法自动关闭，需要 raw-* 追溯继承 platform_ids
- next_action: 已完成（I-20260508T050922Z-A 实现并合并到 develop）
- revisit_trigger: N/A（已 promote 且 completed）
- acceptance_criteria:
  - I-* issue 无 platform_ids 时可追溯 raw-* parent 关闭
  - issue-sync promote 正确写入 platform_ids
- promotion_gate: 修复通过 pre-tests 验证并合并到 develop
- open_questions: []
- acceptance_reviews:
  - reviewer: zhaoquan
  - mode: batch-closeout-round7
  - summary: 修复在 batch round7 中验证通过，issue lifecycle 关闭链路恢复
  - verdict: pass
- promoted_issue_path: docs/issues/I-20260508T050922Z-A/issue.md
- milestone: M-20260508T050922Z-A
- session_refs: []
- completion_note: I-20260508T050922Z-A 已完成 closeout，close 链路修复已吸收到 develop
