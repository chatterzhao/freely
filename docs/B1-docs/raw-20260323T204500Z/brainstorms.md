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

## 2026-03-27 Canonical Develop Recheck

- 这轮直接重读了当前 canonical truth，而不是继续依赖 2026-03-26 replay owner 上的旧冻结结论：
  - `AGENTS.md`
  - `docs/system/workspace/scripts/start-lead-agent.sh`
  - `docs/system/workspace/agents/manager-agent.md`
  - `docs/system/workspace/skills/multi-worktree-supervision/SKILL.md`
  - `docs/system/workspace/three-loop-capability-lifecycle.md`
  - `docs/system/workspace/scripts/runtime/freely`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-capacity-queue`
  - `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-busy-worker-queue`
- 当前 canonical `develop` 已具备这条研究原本要求的最小 contract：
  - worker prompt dispatch metadata 已被要求为 machine-readable runtime contract，而不是补充说明
  - runtime 不再使用固定 numeric worker cap；`manager_max_parallel_workers()` 与 `manager_worker_launch_available_slots()` 当前都返回 `unbounded`
  - launch path 会按 `dispatch_priority` 排序，只在 same-lane busy、`parallel_safe=false` 的单 wave 限制、或 `write_scope` 冲突时把 prompt 留在 queue
  - busy delegated worker 会被 queue，而不是重复 relaunch
- 结论：
  - 这条 pre-brainstorm 的原始问题已经被 canonical `develop` 吸收
  - 当前未收口的不是产品能力，而是旧候选文档还保留着过时 blocker
  - 因此下一跳不是新开平行 issue，而是把 research 真相回写为 `absorbed` supporting evidence；未来若还要继续扩 scheduler，只能以新的、更高阶的 queue/fairness/transaction lifecycle 再开题

## Why now

这不是提速优化，而是自治闭环正确性问题：

- 若 manager 不能在多 worktree 环境下稳定排班，Freely 只能分析，不能真正像“自己开发自己”的项目负责人那样调度。
- 这次 dogfood 暴露的 retained closeout 自环，本质上就是 dispatch contract 缺口的一部分。
