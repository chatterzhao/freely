# 预研：active lifecycle boundary and dogfooding capability discovery

## Context

- 日期：2026-03-21
- 触发：
  - 本轮在用 Freely 开发 Freely 的过程中，反复出现一个判断问题：
    - 什么算“历史”？
    - 什么算“当前仍可修改的真源”？
  - 同时也反复出现一个产品判断问题：
    - 在狗粮过程中暴露出来的问题，是否默认应先视为 Freely 能力缺口？

## Problem

当前仓库里已经有很多 issue、worktree、pre-brainstorm 与 skill。

如果没有明确边界，很容易出现两类错误：

1. 错把仍在活跃生命周期里的东西当历史
- 例如：
  - issue 还在 `in_ibm / in_dev / in_verification`
  - worktree 还没 merge / cleanup
  - 但因为文件较早创建，就误判为“不能再改”

2. 错把已闭环的历史产物当当前承接面
- 例如：
  - issue 已 `completed`
  - 对应 worktree 已收口
  - 却仍把新讨论继续回写到这个历史 issue

还有第三类风险：

3. 狗粮中暴露的问题只被当作一次性经验
- 例如：
  - 当前是 Freely 开发 Freely 时遇到的治理/监督/恢复/路由问题
  - 但没有先判断“这是不是 Freely 本身应该拥有的能力”
  - 结果它只留在聊天或 continuity 中，没有 materialize 为用户也能复用的能力

## Proposed Clarification

### 1. 历史的定义应以生命周期为准，不以时间为准

不是“早创建的文件”就是历史。

更合理的定义是：

- `historical`
  - issue 已走完当前三层 loop
  - 状态已到 `completed` 或等价闭环态
  - 对应 worktree / merge / cleanup 已完成
  - 已不再属于当前活跃执行链

- `active`
  - 仍在当前活跃生命周期里
  - 即使文件创建较早，只要 issue/worktree 还未收口，仍可继续收敛修改

### 2. 当前生命周期内允许应用产物重构

只要当前 issue / worktree 还没收口：

- `pre-brainstorm`
- `candidate`
- `milestone`
- `IBM`
- `dev`
- `verification`

这些当前链路中的真源，都可以继续修改与重构。

重点是：
- 不要在上面记流水账
- 要做应用产物收敛重构
- 让只读局部文件的 AI 也不至于误解边界

### 3. 狗粮中暴露的问题，默认先判断是否应成为 Freely 能力

Freely 开发 Freely 时发现的问题，不应先被当作“项目特例”。

默认应先判断：

1. 这是 Freely 自身独有的偶发细节吗？
2. 还是用户以后用 Freely 开发应用时也会遇到的共性能力缺口？

若属于后者，就应优先视为：
- Freely 的产品能力发现
- 而不是一次性狗粮经验

### 4. 能力实现形态应保持 AI-native

这类狗粮发现出来的能力，不一定表现为传统代码。

它可以 materialize 为：
- agent
- skill
- reference
- runtime script
- hook
- 状态词典/治理规则
- 代码和测试

## Likely Landing

这条预研最终不应停留在原则讨论。

更合理的落点是：

1. 生命周期边界真源
- `docs/system/workspace/three-loop-capability-lifecycle.md`
- 必要时补 `worktree-maintenance-governance`

2. 产品级狗粮逻辑
- `docs/PROJECT_INTENT.md`
- 明确：
  - Freely 开发 Freely 时暴露的可复现共性问题，应优先视为能力发现源

3. 主管判断口径
- `manager-agent`
- `context-source-skill`
- 或相关 routing/reference

## Expected Result

本条预研应最终收敛成：

1. 明确 `historical` 与 `active lifecycle` 的定义
2. 明确“当前生命周期内可重构，历史生命周期只做追溯”
3. 明确“狗粮问题默认先判断是否应成为 Freely 能力”
4. 把这条原则写回适当真源，而不是继续只存在于聊天语境
