# PRD: supervisor 主循环前置 task_mode wait 门禁

## 问题

`task_mode=wait` 启动 Freely 时仍会发射 AI 循环。门禁仅存在于 AI 结束后的
`manager_runtime_handle_exit_contract_after_ai_cycle`（stop_ai handler），
缺少 supervisor 循环在 build prompt / launch AI 之前的前置轮询门禁。

## 方案

在 supervisor 主循环的 `select_launch_kind` 调用之前插入 manager 专属前置门禁：

```
loop {
  read_task_mode_gate()  // 已有，在 stop_ai handler 中
  if task_mode == "wait" {
    sleep(CHECK_INTERVAL)
    continue
  }
  select_launch_kind()   // 已有，不修改
  ...
}
```

## 边界

- task_mode=auto 或 id:<scan-id>：直接通过，行为不变
- stop_ai handler：完全不受影响，保持现有逻辑
- 仅 supervisor 主循环一处修改

## 不涉及

- DB schema 变更
- API 变更
- 配置变更
- 前端变更
