---
issue_id: I-20261124T131119Z-A
issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261124T131119Z/issues/I-20261124T131119Z-A.md
phase_state: completed
---

# Implementation Decision Note
- issue_id: I-20261124T131119Z-A
- issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261124T131119Z/issues/I-20261124T131119Z-A.md
- decision: 新增 issue-sync close-orphans，读取本地映射作为提示后委托 adapter close-local-id，原样汇总并透传 rc。
- why_this: adapter 已拥有枚举真实副本与双平台汇总能力；缺的是可达的封装入口，补入口即可根除手工 adapter 调用诱因。
- alternatives_considered: 放宽 issue-sync close 对 linked 的拒绝——会制造第二套退休判据；让 wt-close 按 [I-*] 标题匹配——身份解析会与 raw 前缀语义冲突。
- boundary_non_goals: 不改 adapter；不改 batch 的 completed 判据；不写本地 frontmatter。
- residual_risk: 平台不可读时 adapter 返回 error，命令非零退出并要求重试；绝不把 error 当 closed。
