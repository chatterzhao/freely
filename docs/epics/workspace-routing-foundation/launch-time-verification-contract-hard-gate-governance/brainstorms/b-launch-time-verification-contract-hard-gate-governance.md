# IBM Brainstorm - launch-time-verification-contract-hard-gate-governance

## Core framing

这条 owner 不再争论“测试是不是重要”，也不把问题继续归因给提示层。核心是把 verification contract 从 record-only 收紧为 launch-time hard gate。

## Candidate implementation shape

### A. Launch boundary

- runtime 在 launch worker 前解析完整 verification metadata
- 缺字段时写 blocked state / missing-fields 诊断
- 不启动 target worker supervisor

### B. Prompt policy

- `Worktree` / `Branch` 仍是 routing 基础
- 但不再足以单独授权 launch
- branch-only / 自然语言 prompt 必须进入显式 remediation，而不是自动放行

## Risks

- 不能误伤完整 metadata 的既有成功路径
- 不能只报一个模糊 failure，必须保留字段级诊断
- 不能把 adequacy schema / retirement enforcement 混进首个实现批次
