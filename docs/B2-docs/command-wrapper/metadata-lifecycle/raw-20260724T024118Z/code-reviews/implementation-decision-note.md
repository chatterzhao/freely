---
issue_id: I-20260724T024118Z-A
issue_path: docs/B2-docs/command-wrapper/metadata-lifecycle/raw-20260724T024118Z/issues/I-20260724T024118Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260724T024118Z-A
- issue_path: docs/B2-docs/command-wrapper/metadata-lifecycle/raw-20260724T024118Z/issues/I-20260724T024118Z-A.md

## Implementation Decision Note

- decision: 契约文档 + 结构校验测试，不动 runtime wrapper 行为
- why_this: 消除元数据生命周期歧义且改动面最小；测试防文档漂移
- alternatives_considered: 仅文档（漂移风险，否）；runtime 强制约束（改动面大且越界，否）
- boundary_non_goals: 不改 runtime/freely wrapper 行为；不重写 verification handoff 契约
- residual_risk: 契约文档为声明式，实际执行仍依赖各流程遵守；后续如需强制可由 Option C 承接
