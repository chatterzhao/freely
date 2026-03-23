# 预研：manager patrol trigger and restart routing

## Context

- 日期：2026-03-21
- 触发：
  - 三层 loop 口径刚补强了 `dev-loop` 的 AI-native 定义。
  - 同时在狗粮开发中反复讨论到一个混淆：
    - 主管不是只做“每轮看一眼”的静态巡检
    - 也不是等用户 chat 才行动
    - 它既有周期巡检入口，也应有事件触发入口
  - 另一个反复出现的混淆是：
    - `verification / writeback / cleanup` 容易被误说成第四层
    - 实际它们仍应属于 `auto-loop` 中主管 watchdog 的持续编排与收口

## Existing Truth Already Present

当前真源里已经有一半答案：

1. `three-loop-capability-lifecycle.md`
- 已定义 `event source`
- 已定义 `standing source`
- 已定义它们汇聚成：
  - `source record -> problem signal -> manager restart-point routing -> delegated loop`

2. `manager-agent.md`
- 已定义主管职责是：
  - 巡检
  - 判断
  - 解释
  - 委派
  - 监督完成
- 已明确主管不直接做 worker 级实现

3. `auto-loop-orchestrator/SKILL.md`
- 已写：
  - 主管同时处理 `event source` 与 `standing source`
  - 对 `standing source` 做周期扫描
  - 对任意 signal 决定 restart point

所以当前缺口不是“完全没有定义”，而是：
- 这些定义还没有被收束成一个清晰、可执行、可持续一致的主管 watchdog 语义

## Problem

当前还存在三个容易混淆的点：

1. `auto-loop` 的触发模型不够清晰
- 有些场景明显属于周期巡检
- 有些场景明显属于事件触发
- 但文档还没有把两者放成同一套主管 patrol contract

2. 主管委派后的回流语义还不够清楚
- worker 做完后，结果应回给主管
- 主管再判断下一步委派到哪一层、哪个起点
- 这点虽然散见于 manager/auto-loop 真源，但还没被总结成清晰 contract

3. restart point 容易被静态化
- 很多讨论默认“从 pre-brainstorm 开始”或“从 dev 继续”
- 但真实情况是：
  - 主管每次收到 signal 后
  - restart point 可能落在 auto/doc/dev 三层中的任意位置

## Research Question

Freely 应如何把主管 watchdog 语义收敛为一条清晰能力：

> 主管既通过 standing-source patrol 周期监督，也通过 event source 被及时唤醒；随后始终只做判断、解释、委派与监督完成，并把下一跳路由到三层 loop 的正确 restart point。

## Proposed Clarification

### 1. 只有三层 loop

- `auto-loop`
- `doc-loop`
- `dev-loop`

不存在“verification/writeback/cleanup 是第四层 loop”的说法。

这些动作应解释为：
- 它们要么是 `dev-loop` 的 worker 执行产物
- 要么是 `auto-loop` 中主管 watchdog 的治理判断与收口动作

### 2. auto-loop 需要双入口

主管 watchdog 至少应有两类入口：

1. `patrol-driven`
- 来源：`standing source`
- 方式：周期扫描
- 典型发现：
  - candidate stuck
  - phase orphaned
  - completion without closure
  - cleanup missing
  - queue/state drift

2. `event-driven`
- 来源：`event source`
- 方式：被 signal 唤醒
- 典型事件：
  - worker 完成阶段
  - worker 发现 blocker
  - test/review 新发现
  - runtime anomaly
  - merge/cleanup 完成
  - human interruption

### 3. 主管总是判断与委派，不直接施工

主管收到 patrol 或 event 后：

1. 解释当前状态
2. 输出：
- `ownership`
- `restart_point`
- `next_action`
3. 委派给：
- analysis worker
- execution worker
- maintenance worker
- runtime owner
4. 等结果回流
5. 再继续下一轮主管判断

### 4. restart point 是动态的

主管每轮都应重新判断下一跳落点，而不是假定总是同一个 loop。

可能落点包括：
- `auto-loop`
  - runtime supervision / cleanup / merge / maintenance
- `doc-loop`
  - pre-brainstorm
  - candidate / milestone intake
  - IBM
- `dev-loop`
  - implementation
  - review
  - verification
  - progress/recovery continuation

## Likely Landing

这条预研不该新造平行 skill。

更合理的承接方式是：

1. 细节真源：
- `docs/system/workspace/three-loop-capability-lifecycle.md`

2. 主管行为真源：
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`

3. patrol reference：
- `docs/system/workspace/skills/multi-worktree-supervision/references/manager-reactivation-patrol.md`

也就是说：
- `three-loop-capability-lifecycle` 负责定义语义模型
- `manager-agent` 负责定义主管职责边界
- `auto-loop-orchestrator` 负责编排口径
- `manager-reactivation-patrol` 负责 patrol reference

## Expected Result

本条预研应最终收敛成：

1. `auto-loop` 的双入口语义被写清
- patrol-driven
- event-driven

2. 主管委派回流 contract 被写清
- 主管解释状态
- 委派 owner
- owner 返回结果
- 主管继续判断下一跳

3. restart point 被明确视为动态决策
- 不预设总是从 pre-brainstorm 或 dev 开始

4. 这些澄清写回现有真源
- 不新增第四层 loop
- 不新增平行 skill
