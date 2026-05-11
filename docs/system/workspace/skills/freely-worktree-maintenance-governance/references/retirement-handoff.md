# Retirement Handoff

用于 historical / companion / obsolete worktree 的收口。

若当前同时涉及多棵 worktree 的保留/合并/清理排序，先做 `fleet_closure` 或 `stacked_merge_chain`，再进入单树 retirement handoff。

## 目标

区分三种情况：

1. `merge whole branch`
2. `salvage_then_retire`
3. `research writeback then retire`

## 必查面

- 当前树是否还有独有能力
- 独有价值是实现、治理边界，还是仅剩 traceability
- 主线是否已有同题能力完成态
- 是否混入跨能力材料，导致整支 merge 会回退主线
- 若是 research worktree，canonical 文档是否已回写：
  - `brainstorms.md`
  - `candidates.md`
  - `docs/milestones.md` candidate / 待研究区

## 输出

- 可摘取的最小差异
- 绝不能整支合并的范围
- retirement 前置条件
- 本地 / 远程 branch disposition
- 若是 research worktree，明确：
  - 已回写到哪些 canonical 文档
  - 哪些结论是 `adopt now / partial adopt / defer / drop`
  - 下次继续研究时应重开新 worktree，而不是保留旧树

## 硬规则

- companion 只能摘自己的历史说明与 traceability，不得再次当主线来源
- obsolete branch 若大部分语义已被主线吸收，只收编独有小能力，然后 retire
- research worktree 默认不长期保留；只要 canonical 文档已完成回写，就进入 `research writeback then retire`
- 若研究结论只有部分可在当前里程碑吸收，当前吸收部分写入正式 issue / milestone，剩余部分继续留在 canonical candidate 区，不以保留旧 research worktree 作为延续方式
- cleanup 前仍必须回到 `skill:freely-branch-management` 的 cleanup lifecycle
- 若远程 branch 仍存在，retirement handoff 必须说明是：
  - 删除 remote
  - 还是保留，并给出明确 blocker / owner / revisit trigger
