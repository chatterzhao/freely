# IBM Brainstorm - pre-tests-cleanup-and-retirement-enforcement-governance

## Core framing

这条 owner 补的是 lifecycle closure 的测试闭环，不是重新设计 completion / merge gate。

## Candidate implementation shape

### A. Retirement gate

- cleanup / retire route 读取 issue-bound `pre-tests.md`
- 未闭环时返回 machine-readable blocker 和 item ids
- tree 保持 retained/followthrough，而不是直接退休

### B. Compatibility

- 第一批只消费最小字段集合
- adequacy schema v2 仍是独立 follow-on

## Risks

- 不能把 deferred gap 误写成 regression
- 不能误改 completion / merge gate
- 不能让 cleanup lifecycle 失去 retained-with-reason 语义
