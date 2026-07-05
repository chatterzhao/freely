# Brainstorm: deep-refactor-fleet-sequencing

- brainstorm_id: `20260326-1825--deep-refactor-fleet-sequencing`
- status: `active`
- created_at: `2026-03-26`
- owner: `codex`
- related_paths:
  - `AGENTS.md`
  - `docs/milestones.md`
  - `docs/progress/workspace-routing-foundation/p-global-ai-account-watchdog-and-manager-bootstrap.md`

## Problem

在开始大重构前，Freely 当前 fleet 里同时存在：

- canonical `develop` manager runtime 处于 `stalled_without_runtime`
- 一棵 `dirty + desired=running` 的 develop-facing merge-prep 工位
- 多棵 `20260326` clean/stopped 上游治理 worktree，部分应先合并给后续工作消费
- root `docs/milestones.md` 落后于若干 closeout / governance worktree 的实际完成状态

如果不先做全 fleet sequencing audit，就直接开深层重构，会把：

- 脏树 closeout
- manager/runtime 恢复
- 上游治理 merge
- 新重构实现

混在一起，导致 owner、依赖与 cleanup judgement 全部失真。

## Evidence

- `git worktree list --porcelain` 当前显示 `develop`、`pre-test-merge` 与 13 棵 feature worktree 并存。
- `./bin/wt-fleet-status` 当前只有两棵 `desired=running` worktree：
  - `develop`
  - `feature/manager-scheduler-capacity-candidate-replay-20260324`
  - 另有一棵 `dirty + desired=running`：`feature/develop-merge-prep-fleet-closure-20260325`
- `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely` 当前显示：
  - `activity_state: stalled_without_runtime`
  - `desired_runtime_state: running`
  - `active_running_worker_count: 2`
  - `active_processes: none`
- `feature/develop-merge-prep-fleet-closure-20260325` 当前 `git status --short` 仍有 6 个未提交文件，且 progress/issue 已明确它仍是 `I-20260318T163000Z` 的 develop-facing closeout owner。
- `feature/ibm-pretests-integration-acceptance-quality-20260326`、`feature/manager-owner-stance-and-source-patrol-20260326`、`feature/freely-layered-architecture-and-tooling-topology-20260326` 相对 `develop` 均为纯前进分支，适合在大重构前作为上游治理批次先合并。

## Thoughtfulness

这里暴露的不是单一 issue，而是大重构前的 sequencing gate 缺失：

1. 不是所有 clean feature tree 都应先完成。
2. 真正高风险的是 `dirty`、`desired=running`、或仍持有 canonical closeout owner 身份的工位。
3. 不是所有上游治理树都同等优先。
4. 若后续大重构会消费新的 IBM/manager 架构规则，应先把这些上游治理线合入 `develop`，否则重构过程会继续按旧 contract 写文档和 closeout。
5. `Freely 自身产品/系统架构` 的高层整理很重要，但它属于开发 Freely 的架构真源，不自动阻塞所有代码级重构；是否前置，取决于这轮重构是否直接改 `AGENTS.md` / `PROJECT_INTENT.md` / `CONSTITUTION.md` / `LAWS.md`。

## Preliminary Decision

大重构前的最小顺序应固定为：

1. 先收束 `feature/develop-merge-prep-fleet-closure-20260325`
   - 它是唯一 `dirty + desired=running` 的工位
   - 且直接承载 `I-20260318T163000Z` 的 canonical closeout / merge judgement
2. 先判清 `develop` manager runtime
   - 若仍要让 Freely 自治消费这轮重构，就不能在 `stalled_without_runtime` 下直接开始
3. 先合并会被其他工作直接消费的上游治理树
   - `feature/ibm-pretests-integration-acceptance-quality-20260326`
   - `feature/manager-owner-stance-and-source-patrol-20260326`
4. 视重构触面决定是否前置合并 `feature/freely-layered-architecture-and-tooling-topology-20260326`
   - 若本轮重构直接改根级开发真源，应先合
   - 若主要改 runtime / implementation，可并行或随后合
5. `feature/closeout-canonical-replay-20260326` 等 clean/stopped closeout tree 不构成大重构前的第一阻塞
6. 只有在以上前置项完成后，才新开 dedicated deep-refactor implementation lane

## Open Questions

- `feature/manager-scheduler-capacity-candidate-replay-20260324` 当前 clean 但仍 `desired=running`；这一问现已收口：canonical `develop` 已吸收 `C-20260323T204500Z-A`，因此它应在大重构前显式 retire，而不是继续作为 retained research owner 留在 fleet 里。
- `develop` runtime 的 `stalled_without_runtime` 是单纯 backlog continuation 积压，还是需要单独恢复动作后才能承接下一轮自治开发？
- 是否要把“pre-refactor fleet sequencing audit”上升为 `LAWS` 级硬约束，而不是只放在 `AGENTS.md` 入口？

## Next Action

- 先把这次 sequencing judgement 固化到 `AGENTS.md` 与 candidate。
- 大重构真正启动前，按本条顺序逐项确认：
  - dirty merge-prep closeout resolved
  - canonical manager runtime healthy or intentionally frozen
  - upstream governance merges absorbed on `develop`
