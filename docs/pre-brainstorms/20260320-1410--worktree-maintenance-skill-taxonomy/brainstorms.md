# 预研：worktree maintenance skill taxonomy

## Context

- 日期：2026-03-20
- 触发：本轮为了核清 Freely 当前所有 worktree 的真实状态，连续做了多轮项目级审计、交叉核对、companion 去重、merge-prep 顺序判断和 research-only 保留判断。
- 已有能力：
  - `skill:branch-management` 负责创建 / 提升 / cleanup 生命周期的大框架
  - `skill:multi-worktree-supervision` 负责项目级排班和 checkpoint / freeze 判断
  - `skill:worktree-hygiene-supervision` 负责 dirty-budget / checkpoint 收口
  - `skill:premerge-reconcile` 负责高风险冲突收敛

## Problem

已有技能能解决：

1. 如何创建或进入正确 worktree
2. 如何看项目级 dirty / checkpoint / runtime 摘要
3. 如何在高风险冲突时做 premerge
4. 如何在满足条件后 cleanup

但缺一层“创建之后的维护能力”：

1. 单个 worktree 的真实状态审计
- 不只看 `milestones.md`
- 还要对齐 `pre-brainstorms / issue / tasks / review / tests / runtime delta`
- 把工位判成：
  - `merge-ready`
  - `research-only`
  - `companion-only`
  - `retire-only`

2. 多个 worktree 的合并预演
- 不是简单看谁 ahead/behind
- 要看共享真源、能力主线、companion 边界、冲突文件、测试回归门
- 给出安全 merge / retire 顺序

3. 历史工位的收编与退休
- 某些工位不能整支 merge
- 只能摘差异或 materialize_then_retire
- 还要明确哪些内容只能保留为 traceability，哪些必须从主线隔离

## Why Existing Skills Were Not Enough

### `branch-management`

它解决“怎么开、怎么合、怎么清”，但不负责：

- 核清一个 worktree 到底是不是已经完成
- companion 是否还能当主线来源
- research worktree 是否只是继续保留而非漏做
- 哪些文件只应人工摘差异

### `multi-worktree-supervision`

它解决“主管如何看多个工位并排班”，但更偏实时调度，不负责：

- 逐棵树做 capability truth reconciliation
- 拉出 merge-conflict surface
- 写出可执行的 merge checklist

### `worktree-hygiene-supervision`

它解决 dirty-budget / checkpoint 问题，但不负责：

- worktree 的文档真相与能力真相是否一致
- 已完成分支为何还不能 merge
- 何时应改判为 retirement / companion

### `premerge-reconcile`

它只在已经进入高冲突预集成时使用，太晚了。
我们这次的大量时间花在进入 premerge 之前：

- 哪些树该 merge
- 哪些树不能 merge
- 哪些树只摘差异
- 哪些树只是 research-only

## Proposed Taxonomy

创建 skill 不应重复 `branch-management`，而应补“维护层”。

建议把维护层拆成三段，由一个专门 skill 统一路由：

1. `worktree audit`
- 输入：一个 worktree
- 输出：真实状态分类 + 还缺什么 + 是否应 merge / keep research-only / retire

2. `merge prep`
- 输入：一组相关 worktree
- 输出：安全顺序、共享真源、冲突面、每步测试门

3. `retirement handoff`
- 输入：historical / companion / obsolete worktree
- 输出：哪些内容要 salvage、哪些绝不能整支 merge、何时可 retire

## Decision

不再新增一个“创建 worktree”技能。

原因：
- 创建与清理入口已经由 `branch-management` 负责
- 本轮真正暴露的缺口发生在 worktree 已存在之后

因此更合适的是新增：

- `skill:worktree-maintenance-governance`

并在其内部明确三种模式：
- `audit`
- `merge_prep`
- `retirement_handoff`

## Acceptance

- 主管在看到“检查所有 worktree / 哪些已完成 / 哪些可 merge / 哪些要退休”这类任务时，有专门 skill 可调用，而不是临时拼接 `milestones + git graph + 经验判断`
- 新 skill 明确说明：
  - 什么时候只看单棵树
  - 什么时候需要跨树合并预演
  - 什么时候只能 salvage_then_retire
- `lead-agent / manager-agent / start-lead-agent.sh` 知道在何时调用该 skill
- 至少有一条脚本级回归锁定这条路由提醒
