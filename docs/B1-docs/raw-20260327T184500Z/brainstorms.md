# Brainstorms - 20260327-1845--manager-consumed-continuity-resume-routing-drift

## Context
- Source: 2026-03-27 在 canonical `develop` 现场观察 `freely start` 后 manager runtime 行为
- Trigger:
  - delegated backlog 已被吸收
  - latest manager continuity 已生成并被 consumed
  - stale worker prompt 指针也已清理
  - 但 manager 没有沿着刚刚 consumed 的 continuity 继续同一条 owner chain，而是重新横向扫描 milestone / issue，开始扩散到低价值 patrol
- User correction:
  - 这类问题不能只作为脚本补丁直接推进
  - 必须先判断它属于 Freely 的哪个 loop / lifecycle，并通过 pre-brainstorm 固定 discovery 边界

## Problem

当前 runtime 已经具备：

- latest continuity generated / consumed truth
- delegated continuation absorption
- semantic loop suspicion surface

但还缺一个更窄的 resume contract：

- 当 manager 已经把当前 continuity consumed 掉，且该 continuity 仍是最新 authoritative truth 时
- 下一轮 manager resume 不应默认回到 generic first-hop patrol
- 它应先沿着 consumed continuity 的 `active_lane / restart_point / next_action / next_supervision_priority` 继续

如果缺少这层 resume anchor，会出现一种新的 drift：

1. runtime cleanup 子任务已经闭环
- continuity consumed
- stale prompt cleared

2. manager 仍继续运行
- 但 prompt 又回到了“先 patrol 全局 standing sources”的首跳语义

3. 结果不是完全 stall
- 也不是 restart storm
- 而是 supervision owner 在同一 issue family 之外横向扩散

## Why This Is Not The Same As Earlier Gaps

- 这不是 `latest generated != latest consumed` 的旧 bug；那条 same-family regression 已修
- 这也不是 semantic loop suspicion 本身；semantic loop 只负责暴露“重复却没前进”的监督信号
- 当前新暴露的是：即使 cleanup followthrough 已经前进，resume 入口仍可能丢掉刚刚 consumed 的 owner chain

## Loop Routing Judgement

- 发现入口：`auto-loop` 现场巡检 / runtime observation
- 当前主题：
  - 先是 runtime continuation / cleanup followthrough
  - 随后暴露出 manager resume drift
- 结论：
  - 它不是独立产品需求
  - 也不是单纯旧 issue closeout 文案
  - 它是 `latest manager continuity consumption` contract 内的 same-family followthrough
  - 这份 pre-brainstorm 的职责已经完成：固定 discovery 边界，并把结论吸收到既有 runtime governance issue family，而不是再 materialize 新 issue

## Initial Hypothesis

最可能的缺口在 prompt composition：

- manager `resume` 时，即使最新 consumed continuity 已存在，prompt 仍默认以 generic lead-agent first-hop framing 开场
- handoff / route-only recovery 有专门的 narrowing 逻辑
- 但 ordinary consumed-continuity resume 没有对应 narrowing contract

## Expected Capability Direction

如果这条方向成立，最小能力应是：

1. 只在 manager `resume` 且当前 consumed continuity 仍等于 latest generated truth 时生效
2. 只对 manager-owned `completion_verification` / `cleanup_governance` 这类 closeout chain 做 resume narrowing
3. 一旦出现 fresh delegated continuation、authoritative fleet contradiction、或 restart point 已关闭，就重新放回 full patrol

## Separation From Merge-Gate Coverage

- 本轮还同时暴露了另一条问题：merge gate 没能拦住“未按三层 loop 正常 materialize 的修复”
- 那条问题不是本 pre-brainstorm 的主主题
- merge gate 覆盖缺口应回到现有 `20260321-1835--lifecycle-complete-before-merge-governance` 方向重新判断是否 reopen / materialize
