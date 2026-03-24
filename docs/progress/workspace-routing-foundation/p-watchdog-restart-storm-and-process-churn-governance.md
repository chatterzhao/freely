# Progress: watchdog-restart-storm-and-process-churn-governance

- issue: `I-20260324-0405`
- title: Watchdog restart-storm and process-churn governance
- phase_state: `completed`
- runtime_state: `closed_for_this_batch`
- summary: 已完成 watchdog restart-storm / process-churn 的 runtime 实现与验证：短窗口 signal 写入 `session-state.env`，watchdog 命中后暂停 blind relaunch 并升级给 manager，`live-status` / `fleet-status` 已暴露摘要；issue 完成，但 worktree 仍待 merge / cleanup / retirement。
- completed:
  - freeze raw signal truth in `session-state.env`
  - freeze no-mirror rule for `workcell-state.env`
  - freeze manager-owned judgement contract
  - freeze default thresholds
  - implement restart-storm/process-churn runtime helpers and persisted signal fields
  - expose signal summary in `live-status` / `fleet-status`
  - add runtime tests for signal emission, no-mirror, escalation, and blind-relaunch pause
- next:
  - merge this worktree into `develop`
  - continue cleanup / retirement gating before deleting the worktree or branch
