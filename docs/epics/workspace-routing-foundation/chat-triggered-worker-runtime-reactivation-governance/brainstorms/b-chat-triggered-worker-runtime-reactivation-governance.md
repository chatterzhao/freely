# IBM Brainstorm: chat-triggered-worker-runtime-reactivation-governance

## Core Question

当 worker 工位已经 `operator_stop`，但用户继续通过 `freely chat` 给当前 active issue 插话时，Freely 应该只是 durable intake，还是要把 worker 主循环重新拉起？

## Answer

对于明确属于本工位继续推进的 delegated continuation / verification handoff，应该重新拉起 worker 主循环。

否则 `chat` 只会形成“假活性”：
- signal 被接住
- dispatcher 也有反应
- 但真正做事的 worker loop 没有回来

## Boundary

- 不是所有 chat 都自动拉起完整 runtime。
- 只有当 interruption classification 已经收敛到：
  - worker-owned
  - current workcell should continue
  - 当前没有 active AI/supervisor
- 才触发 reactivation。

## Non-Goals

- 不在本 issue 重写 manager/worker 角色。
- 不把 `freely intake chat` 变成高层入口。
- 不通过 PTY 注入去复活已经结束的进程。

## Likely Implementation Direction

1. `freely chat` 继续：
   - bootstrap minimal interruption control plane
   - durable write intake
   - run interruption classification
2. 若 classification 结果是 worker-local continuation / verification，且当前 runtime stopped：
   - 触发 worker runtime reactivation preflight
   - 拉起主循环
3. 主循环再消费 delegated intake，并回到正确的 restart point。
