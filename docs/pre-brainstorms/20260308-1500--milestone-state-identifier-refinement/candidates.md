# Candidates: 里程碑状态标识符语义收敛

## C-20260308-1501

- title: 里程碑状态标识符重命名与职责边界收紧
- status: proposed
- decision_reason: 当前 `milestone_state=in_progress` 与 `loop_stage` 存在语义重叠，`in_progress` 命名不够自解释
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- acceptance_hint: 1) LAWS 2C 更新流程标识词典，将 `in_progress` 改为 `active`，`completed` 改为 `delivered`；2) milestones.md policy 同步更新；3) 所有现有 issue 文档迁移状态标识；4) skills 引用更新
- scope:
  - LAWS 2C 流程标识词典
  - milestones.md milestone_state_policy
  - 所有 docs/epics/**/issues/*.md 状态字段
  - 相关 skills 状态判断逻辑
- impact: 中等 - 需要更新多个文档，但语法层面兼容（只是值域变化）
