---
issue_id: I-20261101T124657Z-A
issue_path: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T124657Z/issues/I-20261101T124657Z-A.md
phase_state: in_progress
---

- issue_id: I-20261101T124657Z-A
- issue_path: docs/B2-docs/dsh-plugin/freely-host/raw-20261101T124657Z/issues/I-20261101T124657Z-A.md

## Implementation Decision Note

- decision: 确定性 DSH plugin driver，直接建 worker/reviewer session；E2E-worker preset 带 bash，产品 P1 preset 不动。
- why_this: 模型自由编排不可判定；fake ctx 不能证明真实 DSH session。
- alternatives_considered: 模型驱动 Manager（拒绝）、只 fake ctx（拒绝）、改 P1 worker 加 bash（拒绝）。
- boundary_non_goals: 不改 P1；不做 Panel/多项目；不做 ACP。
- residual_risk: DSH private API；模型可能不按 task 执行；E2E 依赖真实 model/账号。
