# IBM Brainstorm: deep-refactor-fleet-sequencing-governance

## Stable Scope

- 这条 issue 解决的是开发 Freely 的 sequencing gate，而不是运行期能力缺口。
- 最小稳定改动面已经确定为 `AGENTS.md` 加 lifecycle writeback，不需要扩大到 `docs/system/**`。
- verification 以真实 fleet audit 与实际收束动作为证据，而不是只做 wording review。

## Boundaries

- 允许：
  - 写明 broad/deep refactor 前必须执行的 fleet audit
  - 写明 dirty/running/owner 工位优先于 clean/stopped 工位
  - 写明 upstream governance merge 的最小前置顺序
- 不允许：
  - 把这条规则上升成 Freely 产品能力真源
  - 借机重写 unrelated runtime / watchdog 逻辑
  - 把所有 existing worktree 都纳入同一大清理 issue

## Implementation Shape

1. 在 `AGENTS.md` 增加 pre-refactor sequencing gate
2. 在 lifecycle 文档中冻结 acceptance / verification
3. 用真实 fleet audit 与 merge-prep / stop 动作证明这条 gate 已经可执行
