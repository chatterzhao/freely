# IBM Brainstorm: latest-manager-continuity-worker-consumption-governance

## Core Decision

不要再把 worker launch / reentry 是否需要执行，绑定到“之前曾消费过某个 prompt 文件”的旧快照上。canonical 事实应是：

1. latest continuity generated
2. latest prompt set generated from that continuity
3. latest continuity / prompt set consumed by runtime

## Why Existing Runtime Falls Short

- `manager_runtime_launch_workers_from_latest_handoff()` 已存在，但当前没有接在主管 watchdog 的主路径上。
- 因此只有某些恢复路径会触发 worker launch/reentry。
- 当主管已经在运行且产生了更新的一轮 continuity 时，runtime 可能根本不去消费它。

## Materialization Shape

- runtime:
  - call latest-consumption logic from `ensure_manager_once`
  - write generated/consumed launch state
- observability:
  - baseline/live status expose the generated/consumed truth
- tests:
  - stale state update
  - already-running manager path

## Non-Goals

- 不改 interruption triage 分类
- 不改 manager disposition 语义
- 不引入外部 TUI 驱动
