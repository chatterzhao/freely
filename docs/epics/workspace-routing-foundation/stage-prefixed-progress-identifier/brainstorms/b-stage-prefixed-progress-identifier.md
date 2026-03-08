# Brainstorm: stage-prefixed-progress-identifier

## Focus

把“阶段前缀式进度标识”从 pre-brainstorm 收敛为正式治理 issue，明确主词典与字段边界。

## Key Decisions

1. 主进度标识采用 `phase_state=<prefix>_<stage>`。
2. `pending_*` 不进入主进度词典；未开始但可推进统一用 `todo_*`。
3. `milestone_state` 只保留队列归属，不再表达 IBM/dev 阶段。
4. 阶段前缀固定为 `todo_*`、`in_*`、`done_*`、`blocked_*`；`completed` 只用于整个 issue 生命周期终态。
5. `done_ibm` 作为 IBM->dev handoff 真源；不保留 `ready_for_dev`、`todo_for_dev` 或 `pending_*`。

## Open Checks

1. `phase_state` 是替换 `loop_stage`，还是由 `loop_stage` 迁移兼容到 `phase_state`。
2. `blocked_*` 是否只对 `dev` 开放，还是允许更通用的阶段阻塞表达。
3. 现有 issue / milestone / progress 文档的迁移顺序如何定义，才能避免一半新词典、一半旧词典并存。
