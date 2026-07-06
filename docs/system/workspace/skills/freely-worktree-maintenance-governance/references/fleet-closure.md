# Fleet Closure

用于项目级 worktree 治理收口，不是只看单棵树，而是检查当前所有 active worktree 的生命周期、合并链和 cleanup readiness。

## 目标

输出一份仓库级 closure inventory，而不是只回答“现在要不要 merge 这棵树”。

每轮至少要把每个 active worktree 归入以下之一：

1. `continue-dev`
2. `merge-up`
3. `merge-prep-to-develop`
4. `research-writeback-then-retire`
5. `retire-now`
6. `blocked`

## 输入

- `git worktree list --porcelain`
- `freely wt-status-all`
- 每个 active worktree 的：
  - branch / execution base / integration target
  - clean / dirty
  - source pre-brainstorm / candidate / milestone / issue
  - review / tests / verification evidence
  - 是否已经进入 `develop`

## 必查面

1. Canonical lifecycle
- pre-brainstorm 是否存在
- `candidates.md` 是否存在且记录准确
- promoted candidate 是否已经 materialize 到正式 issue
- issue 是否进入 milestone，并与 `phase_state` 对齐
- `completed` 是否真的有实现 / review / test / verification 证据

2. Git / merge truth
- worktree 是否 clean
- branch 是否已经被 `develop` 吸收
- 若依赖父 feature，是否已经显式按 `child -> parent -> merge-prep-from-develop -> develop`
- 是否存在 merge-prep 暴露的新 integration fix

3. Retirement truth
- 是否已经 `verified-retirable`
- 是否还留有未吸收独有能力
- 是否只是 research container，canonical writeback 已完成
- 本地 branch / 远程 branch 是否都已进入明确 disposition

## 输出

1. fleet inventory
2. 本轮可闭环的 merge / cleanup 列表
3. 本轮必须保留为 active / blocked 的 worktree 列表
4. 对每条 parent-child chain 的逐层 merge 顺序
5. 对 cleanup 的明确 gate：
  - 只有 `verified-retirable` 才能删除 worktree / branch
  - 若存在远程 branch，必须明确 `deleted` 或 `retained with reason`

## 持续治理规则

- fleet closure 是持续治理，不是“本轮必须把所有 worktree 清空”。
- 当前仍在开发、仍有 candidate 未收口、或因外部依赖阻塞的 worktree，可以继续保留为 active。
- 但它们不得从视野中消失；必须显式写出：
  - 当前 disposition
  - blocker / next_action
  - revisit_trigger

## 硬规则

- 不允许把“已经 merge”当作治理结束；还必须判断能否 cleanup。
- 不允许把“本地已经 cleanup”当作退休完成；若远程 branch 仍存在，必须明确删除或记录保留原因。
- 不允许为了追求仓库干净而强行关闭仍在开发中的 worktree。
- 不允许把 dirty merged branch 直接删掉；先判断是否有未吸收差异。
- 不允许把 candidate/issue 生命周期不完整的 worktree 误判为 `retire-now`。
- 不允许跳过 parent 或 merge-prep，直接宣称 feature 可并入 `develop`。
