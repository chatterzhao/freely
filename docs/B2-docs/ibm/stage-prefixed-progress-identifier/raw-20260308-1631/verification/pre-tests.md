# Pre-Tests: stage-prefixed-progress-identifier

1. 任何主进度状态值都能从单个值看出所处阶段，不再依赖 `in_progress` + 额外字段拼读。
2. 未开始但可推进的阶段使用 `todo_*`，不出现 `pending_*` 主状态。
3. 若 item 因外部条件无法推进，使用 `blocked_*` 或等价独立字段，而不是 `pending_*`。
4. `milestone_state` 与主进度标识职责分离，不再用 `in_progress` / `completed` 表达阶段。
