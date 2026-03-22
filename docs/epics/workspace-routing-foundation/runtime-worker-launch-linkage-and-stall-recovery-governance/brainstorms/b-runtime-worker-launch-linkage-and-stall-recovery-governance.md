# IBM Brainstorm - runtime-worker-launch-linkage-and-stall-recovery-governance

## Core framing

这条 issue 的核心不是“manager 还能再怎么写 prompt”，而是：

- runtime 如何把 manager 已经产出的 stable worker handoff 变成 worker execution
- runtime 如何在当前 AI 轮次挂起时把新的 delegated continuation 重新带回主循环

## Candidate implementation shape

### A. Worker launch linkage

建议把 manager handoff 变成：

- target worker worktree 的 delegated continuation intake
- target worker `DESIRED_RUNTIME_STATE=running`
- manager runtime / watchdog 启动该 worker supervisor

这样 worker 仍走现有：

- prompt build
- delegated continuation absorption
- session resume / fresh_with_handoff

而不是引入一条平行启动链。

### B. Stalled AI recovery

最小 stall 信号：

- ai pid 存活
- 当前 cycle log 在阈值内无更新
- 新 intake 创建时间晚于当前 cycle start 或 delegated continuation 仍 pending

恢复动作：

- graceful TERM
- 超时 hard-kill fallback
- 写 `preemption-state.env`
- 由 supervisor 下一轮继续消费

## Risks

- 不能误把正常长跑 AI 当成 stall
- 不能因为 manager handoff parsing 脆弱而起错 worker
- 不能把 target worker intake 写到错误 worktree
