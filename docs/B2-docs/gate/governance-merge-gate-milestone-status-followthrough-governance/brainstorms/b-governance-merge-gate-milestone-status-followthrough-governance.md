# Brainstorm: governance-merge-gate-milestone-status-followthrough-governance

## Problem Slice

当前问题已经缩到一条明确 parser bug：

- milestone 顶层 `- status: active`
- nested `candidate_issues` item `- status: needs_research`
- `parse_milestones()` 却把后者覆盖到前者

这让 active candidate placement gate 误报，不是 policy 争议，而是层级解析失真。

## Chosen Direction

1. 在 `parse_milestones()` 中只在 milestone 顶层、且尚未进入 queue item 时读取 milestone `status`。
2. 保持 queue item 其他字段解析不变，只修正 milestone status 污染。
3. 用单条 focused regression 锁住 `active milestone + nested candidate status` 的通过路径。

## Excluded Paths

1. 不重写 `docs/milestones.md` 语法。
2. 不把 queue item status 本身纳入新的语义判断。
3. 不改变 active candidate 必须绑定 active milestone 的规则。
