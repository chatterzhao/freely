# Brainstorms - 20260320-0908--research-candidate-persistence-governance

## Trigger

- 在逐个清查现存 worktree 时发现，部分研究项当前还不能 materialize 或收口，但现有治理只写了 `candidate -> milestone -> IBM`，没有强制要求“本轮不继续做时也必须显式保持可见”。
- 用户要求：不能因为没有明确继续研究或继续收口，就在后续扫描里跳过这些项。

## Problem

当前 Freely 已经有 `needs_research`、`blocked`、`candidate_issues` 等状态词，但缺少一条更明确的治理约束：

1. 研究项当前不能收口时，应该停在哪个队列。
2. 下一轮主管如何知道它不是“已完成”或“可忽略”。
3. 什么时候应该重新启动研究，而不是无限悬空。

如果没有这条约束，主管扫描很容易只盯 `committed_issues` 或当前正在推进的实现分支，把仍未闭环但已经识别过的能力缺口漏掉。

## Boundary

本轮先收敛治理与可见性，不扩成新的 runtime 控制面：

- 定义 unresolved candidate 的最小记录字段
- 定义它在 `docs/milestones.md` 中必须保持可见
- 定义 lead/manager 首跳扫描时不能静默跳过
- 暂不新增数据库、额外状态机或自动提醒服务

## Expected outcome

- `three-loop` 真源明确写出 unresolved candidate persistence 规则
- `doc-pre-brainstorm` skill/reference 要求写 `next_action` 与 `revisit_trigger`
- 首跳 prompt 明确：不能因为本轮不推进就跳过研究项
- `docs/milestones.md` 对 `needs_research` / `blocked` 的可见性要求更清楚

## Next route

- 继续 pre-brainstorm，若这套规则在 lifecycle + prompt + tests 落地后仍发现边界不足，再 materialize 成独立 issue
