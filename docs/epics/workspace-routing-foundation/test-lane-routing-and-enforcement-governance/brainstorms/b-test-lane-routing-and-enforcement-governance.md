# Brainstorm: test-lane-routing-and-enforcement-governance

## Decision

把测试 lane 约束 materialize 成独立 owner，而不是继续作为 promote-gate owner 的隐含扩张。

## Why This

1. `test-pre-merge` promote source semantics 已经由 1615/1805 两条 owner 冻结。
2. `test-lane` 解决的是“测试命令在哪种 branch/worktree 上跑才算合规”，这是相邻但不同的治理面。
3. 当前仓库已出现裸实现、入口不可执行、branch family 过宽、旧语义参考未同步等多点漂移，需要统一收口。

## Frozen Boundary

本 owner 解决：

1. lane truth
2. wrapper entrypoint correctness
3. machine enforcement
4. focused regression alignment

本 owner 不解决：

1. automatic lane inference
2. batch create UX
3. lifecycle automation
4. runtime lane visualization
