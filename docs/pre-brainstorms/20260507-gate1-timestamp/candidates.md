# Candidates

## C-20260507T0300Z-A: GATE 1 分支名时间戳一致性校验

- candidate_format_version: v2
- title: GATE 1 pre-merge 门禁增加分支名时间戳与 governance chain 一致性校验
- status: promoted
- promoted_issue_path: docs/issues/I-20260507T0300Z-A/issue.md
- decision_reason: 时间戳一致性是治理可追溯性的基础；不一致的分支名会导致审计困难和工作流混乱；作为 GATE 1 门禁的补充校验，实现范围清晰、风险低
- milestone: M-20260507T0300Z-A
- acceptance_criteria:
  - GATE 1 校验分支名时间戳与关联 issue 创建时间或 worktree 创建时间对齐
  - 时间戳不匹配时门禁拒绝通过并给出明确错误信息
  - 不破坏现有 GATE 1 其他校验逻辑
