# 研究：manager worker scheduler capacity and queueing

## Context

- 日期：2026-03-23
- 触发：真实 dogfood 中，manager 已经能把 retained continuation、cleanup queue、以及新插话 discovery 同时看见，但仍会把后续动作挤回单一 continuation lane。
- 已知事实：
  - `lead-agent`、`manager-agent`、`multi-worktree-supervision` 都明确写了“可并行则并行”。
  - `start-lead-agent.sh` 只要求产出 manager continuity 和 worker prompt set，但没有强制 worker prompt 带 dispatch metadata。
  - `runtime/freely` 会线性消费 continuity 中的 worker prompt 路径，没有 worker capacity、queue、busy-worker reentry guard。

## Problem

当前 gap 不是“manager 不知道应该并行”，而是：

1. manager prompt contract 没把 lane 排班写成 runtime 可消费的元数据；
2. runtime 也没有 capacity-aware launch/queue 机制；
3. active worker 已在处理 delegated continuation 时，manager 还能重复向同一 worktree 写入新的 launch intake。

结果是：

- clean merged tree 的 cleanup lane 不能及时独立推进；
- 新插话要求 fresh worktree 的任务会被旧 continuation 拖住；
- worker prompt set 退化成“无序 prompt 列表”，而不是 fleet scheduler 的派工计划。

## Convergence

这条线应收成一个最小闭环，而不是再发明平行 skill：

1. manager/lead prompt contract：
   - 每个 worker prompt 至少带 `dispatch_priority`、`parallel_safe`、`write_scope`
   - capacity 不足时，把未派发 lane 保留在 continuity queue，而不是静默丢失
2. runtime launch contract：
   - 按 priority 选 prompt
   - respect worker capacity
   - 对 active delegated worker 做 busy guard，避免重复 launch spam
   - 记录 queued worker prompts 供 `live-status` / `baseline-status` 观察
3. lifecycle 真源：
   - 把 queue/capacity 联动写进 `three-loop-capability-lifecycle`

## Why now

这不是提速优化，而是自治闭环正确性问题：

- 若 manager 不能在多 worktree 环境下稳定排班，Freely 只能分析，不能真正像“自己开发自己”的项目负责人那样调度。
- 这次 dogfood 暴露的 retained closeout 自环，本质上就是 dispatch contract 缺口的一部分。
