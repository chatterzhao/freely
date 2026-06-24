## Implementation Decision Note
- issue_id: I-20260624T072546Z-A
- issue_path: docs/issues/I-20260624T072546Z-A/issue.md
- decision: 所有用户可见报错去平台硬编码，统一指 feedback --help
- why_this: 平台通过 adapter 抹平，报错不应假定具体平台
- alternatives_considered:
  1. 保留 GitHub 示例 + 加 Gitee — 每加一个平台都要改报错，不可持续
  2. 全删 — 用户不知道下一步做什么
  3. 指向 --help — 平台无关且可操作
- boundary_non_goals: 不改 feedback 实现层（仍用 gh CLI）
- residual_risk: 无
