---
name: freely-worktree-maintenance-governance
description: >- 核清单个 worktree 真实状态、制定多条 worktree 安全 merge 顺序、
  处理 stacked merge-chain、做 fleet closure 审计、处理 retired worktree。

  Use when: 主管需要做 worktree 级别的维护决策和审计。
  触发词："worktree maintenance"、"工位维护"、"fleet audit"、
  "merge order"、"retire"、"salvage"。
---

# skill:freely-worktree-maintenance-governance

## 何时使用

- 需要判断某个 worktree 是 `merge-ready`、`research-only`、`companion-only` 还是 `retire-only`
- 需要为一组相关 worktree 做 merge-prep，而不是只看 milestone
- 需要处理“不是直接从 develop 派生”的 child/parent 链路，并判断是否必须先向上逐层合并
- 需要检查当前所有 active worktree 的 lifecycle / merge / cleanup 状态，并决定这轮哪些该继续、哪些可 merge、哪些可 retire
- 需要处理 historical / companion / obsolete worktree 的差异摘取与 retirement handoff

## 模式选择

1. 单棵树真实状态核对：读 [references/audit.md](references/audit.md)
2. 多棵树合并预演：读 [references/merge-prep.md](references/merge-prep.md)
3. 存在父子依赖的逐层合并：读 [references/stacked-merge-chain.md](references/stacked-merge-chain.md)
4. 项目级 fleet 审计与 closure：读 [references/fleet-closure.md](references/fleet-closure.md)
5. 历史工位收口与退休：读 [references/retirement-handoff.md](references/retirement-handoff.md)

## 工作流

1. 先跑 `skill:freely-constitution-guard` 和 `skill:freely-laws-enforcer`
2. 若当前承担项目级判断，先结合 `skill:freely-multi-worktree-supervision` 读取工位总览
3. 再根据当前问题选择 `audit / merge_prep / stacked_merge_chain / fleet_closure / retirement_handoff`
4. 结论必须落成清晰分类或顺序：
   - `merge-ready`
   - `research-only`
   - `companion-only`
   - `retire-only`
5. 对进入 retirement / cleanup 的分支，必须同时给出本地与远程 branch disposition：
   - `deleted`
   - `retained-with-reason`
5. 若问题只是创建/进入/删除 worktree，回到 `skill:freely-branch-management`
6. 若问题已经升级为高风险文本冲突收敛，切到 `skill:freely-premerge-reconcile`
7. 若是仓库级 fleet closure，必须允许“本轮只闭环其中一部分 worktree”；未闭环工位继续保留可见 disposition，而不是为了追求清空而误删

## Research worktree policy

- `research-only` 指研究结论当前只保留在 canonical 文档，不指“长期保留这棵 research worktree”。
- research worktree 是一次研究执行容器；研究完成后，默认把结论回写到：
  - `docs/pre-brainstorms/<id>/brainstorms.md`
  - `docs/pre-brainstorms/<id>/candidates.md`
  - `docs/milestones.md` 的 candidate / 待研究区域
- 回写完成后，research worktree 默认进入 `retirement_handoff`，不长期挂在项目里。
- 若后续继续研究同一主题，应重新创建新的 dedicated worktree，并继续更新原 canonical brainstorm/candidate，而不是复活旧 research worktree。

## 边界

- 不替代 `freely-branch-management` 的创建、promotion 和 cleanup 基础命令
- 不替代 `freely-worktree-hygiene-supervision` 的 dirty-budget / checkpoint 收口
- 不替代 `freely-premerge-reconcile` 的冲突修复
- 不允许只凭 `milestones.md` 单独下结论
- 不允许只按提交先后、分支新旧或“谁更接近 develop”决定保留哪套行为；遇到相近能力时必须先做 anti-retrogression 比较，保留更好的设计、验证门和用户语义
- 不允许 child worktree 在存在明确 parent 依赖时，跳过 parent 直接声称可并入 `develop`
- 不允许把“已 merge 但未 cleanup”当作 fleet closure 完成；cleanup 仍需过 `verified-retirable`

## 完成

- 当前问题已被稳定分类，或已有可执行的 merge / retire checklist
- companion / research / completed 的边界不再混淆
- 若是 fleet closure，当前 active worktree 都已有明确 disposition、下一步和 cleanup gate
- 若进入 cleanup，远程 branch disposition 也已明确，而不是只删除本地 worktree
