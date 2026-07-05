# PRD: stage-prefixed-progress-identifier

## Goal

让 Freely 的主进度标识从“泛化进行中”转为“值本身即可读出阶段”的规范语法。

## Requirements

1. 明确主执行标识采用阶段前缀语法，而不是 `in_progress` / `active`。
2. 主词典不采用 `pending_*` 作为未开始状态。
3. `todo_` / `in_` / `done_` / `blocked_` 的边界必须清晰可路由。
4. `milestone_state` 保持队列归属语义，不再承载执行阶段。
5. 字段迁移方案需能落到 `LAWS`、`milestones.md`、issue/progress/recovery 与核心 skills。
