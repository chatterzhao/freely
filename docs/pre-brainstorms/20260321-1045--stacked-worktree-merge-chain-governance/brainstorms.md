# 预研：stacked worktree merge-chain governance

## Context

- 日期：2026-03-21
- 触发：本轮在 `cc-use-codex-cli` 相关工位上实际经历了：
  - 子分支依赖未进入 `develop` 的父分支
  - 需要先把子分支合回父分支，再判断父分支是否能继续向 `develop`
  - 父分支 dirty / 未提交 skill / pre-brainstorm 会阻断下一级合并
  - 基于最新 `develop` 的 merge-prep worktree 会暴露新的集成问题与治理索引冲突

已有 `skill:worktree-maintenance-governance` 已覆盖：

- 单棵树真实状态审计
- 多棵树 merge-prep
- retirement handoff

但本轮证明还缺一层更明确的“派生链路治理”。

## Problem

当前 skill 对“多棵树合并预演”的定义仍偏平面化，不足以稳定指导这种场景：

1. worktree A 依赖父分支 B，而 B 还没进 `develop`
2. A 自己已 clean / tested / docs-complete，但 B 仍 dirty 或 governance 未承接
3. 把 A 合回 B 后，B 再合向 `develop` 时可能出现新的治理索引冲突或 integration bug
4. 最终需要的不只是一个 merge-ready / retire-only 判断，而是一整条：
   - `child -> parent -> merge-prep-from-develop -> develop`

## Discovery From This Run

这次实际暴露出 5 个应该收敛成 skill 规则的点：

1. 依赖链识别
- 不能只看当前分支是否 clean
- 必须识别：
  - 当前分支的 merge-base
  - 直接父分支
  - 父分支是否 clean
  - 父分支是否已 materialize 必要治理产物

2. 逐层 merge gate
- `child -> parent`
- `parent -> merge-prep-from-develop`
- `merge-prep -> develop`

每一层 gate 至少要看：
- docs / candidate / milestone / issue 状态
- git cleanliness
- tests
- live smoke / integration evidence
- conflicts 是否只是 additive governance conflict，还是实质代码冲突

3. parent branch hygiene 也是 gate
- 子分支完成并不代表可直接继续
- 若父分支 worktree 自己 dirty，必须先收口父分支，再接 child merge

4. merge-prep worktree 是正式步骤，不是临时技巧
- 对基于旧 develop 派生的复杂链路，应该显式开一棵：
  - `feature/merge-prep-*`
- 它的职责是：
  - 合入最新父分支
  - 解 additive 治理冲突
  - 跑集成回归
  - 暴露 develop 侧才会出现的问题

5. 集成问题可能属于 develop 当前面，而不是 child branch
- 本轮真实暴露：
  - `status --view all` 在 `set -u` 下因空数组展开失败
- 这类问题不应被误记为 child 分支未完成
- 应记录为：
  - merge-prep 阶段发现的 integration fix

## Proposed Skill Evolution

不新造一个完全独立的新技能。

更合理的是扩展现有：
- `skill:worktree-maintenance-governance`

新增一个更明确的模式或子章节：
- `stacked_merge_chain`

其输入不是“单棵树”或“平面的一组树”，而是：
- 当前目标分支
- 直接父分支
- 最终 integration target（通常是 `develop`）

其输出应该是：
- 派生链图
- 每一层 gate 结果
- 当前阻塞点
- 下一棵必须处理的 worktree
- 是否需要新建 merge-prep worktree
- 若 merge-prep 发现集成问题，应把问题归属到哪一层

## Candidate Direction

最值得 materialize 的不是“再发明一个 branch-management 变体”，而是：

- 扩展 `skill:worktree-maintenance-governance`
- 让它明确支持：
  - stacked dependency chain
  - parent-first merge rule
  - merge-prep-from-develop gate
  - integration-fix attribution
  - cleanup only after upper layer is also safe

## Acceptance Sketch

- skill 能明确判定“必须先合 child 到 parent，不能直接碰 develop”
- skill 能在 parent dirty 时阻止继续往上 merge
- skill 能要求显式创建 merge-prep worktree，而不是在 develop 主工位直接试合
- skill 能区分：
  - additive governance conflict
  - real code conflict
  - merge-prep 新发现的 integration bug
- skill 能给出完整链路 checklist：
  - child readiness
  - parent readiness
  - merge-prep readiness
  - final cleanup readiness

## Immediate Next

- 在本 pre-brainstorm 下形成 candidate
- 后续如被接纳，进入 `worktree-maintenance-governance` 的下一轮增强，而不是散落到临时 review 经验里
