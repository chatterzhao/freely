# Brainstorm: manager-delegation-after-sufficient-patrol-evidence-governance

## 核心边界

这条 issue 不再讨论：

- manager 能否接住新的 signal
- manager continuation handoff 是否生成/消费
- manager patrol 有没有基本 worktree 审计能力

这些都已经分别由已有 lifecycle 覆盖。

这条 issue 只讨论：

**当 manager 已经拿到足够证据，何时必须停止继续 patrol，并进入具体 worker delegation。**

## 收敛结论

1. `patrol` 是为了形成 disposition，不是为了无限制补充佐证。
2. 当以下三元组已经稳定时：
   - `ownership`
   - `restart_point`
   - `next_action`
   主管就应转入具体 worker handoff。
3. 只有在以下情况才允许继续 patrol：
   - 关键事实缺失
   - 上下游依赖未明
   - disposition 之间仍冲突
   - cleanup / continue-dev 的进入条件尚未达到
4. 若 `retire-only / retire-now / continue-dev` 已明确，但主管仍继续 manager-only 巡检，则属于监督退化。
