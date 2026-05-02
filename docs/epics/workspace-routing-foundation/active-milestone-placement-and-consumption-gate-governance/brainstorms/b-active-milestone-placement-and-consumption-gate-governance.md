# IBM Brainstorm: active-milestone-placement-and-consumption-gate-governance

## Owner Cut

`C-20260331-2012-A` 已经把问题边界冻结清楚：不是继续发明新的 milestone 排期引擎，而是把当前仓库已经接受的治理约束真正落到 quality gates。

当前 owner 只处理最小可验证闭环：

1. active candidate 不能保持 `milestone: unassigned` 或 `pending://...`
2. unresolved `needs_research | proposed | blocked` 必须留在 active milestone 的 `candidate_issues`
3. candidate 文档里的 `milestone:` 必须与 `docs/milestones.md` 的实际承接 `M-*` 一致
4. completed milestone 默认不再承接新的 unresolved candidate
5. `promoted` candidate 必须 materialize 成 formal `I-*` sequencing，而不是继续伪装成长期 candidate

## Why This Slice

当前仓库已经出现过两类真实问题：

- 重要 candidate 仍是 `unassigned` 或 `pending://milestone-binding`
- candidate 形式上“在某个 milestone 里”，但仍可能挂进错误或不会消费的 lane

因此最小 owner 应优先把 placement correctness 变成 gate，并把相关真源与现存 backlog 对齐，而不是继续扩大到完整排期策略。

## Out Of Scope

1. 不实现 milestone 子阶段排序系统或 `M1.1 / M2.1`
2. 不把所有历史 candidate 全部重写成新的 placement schema
3. 不在同一 owner 内继续实现 runtime 自动消费/自动迁移排程器
