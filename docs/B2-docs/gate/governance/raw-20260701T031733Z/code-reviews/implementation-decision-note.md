---
issue_id: I-20260701T031733Z-A
issue_path: docs/B2-docs/gate/governance/raw-20260701T031733Z/issues/I-20260701T031733Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260701T031733Z-A
- issue_path: docs/B2-docs/gate/governance/raw-20260701T031733Z/issues/I-20260701T031733Z-A.md

## Implementation Decision Note

- decision: 修改 5 个 skill 文档的模板/示例/检查清单，对齐 gate 期望
- why_this: 源头修正最有效——3 个 PR 的 15+ 次 gate 失败均源于 skill 模板不完整
- alternatives_considered:
  - 只加 pre-flight 代码不改 skill: 治标不治本
  - 只改 skill 不加 pre-flight: 本轮方案，后续再评估 pre-flight
- boundary_non_goals: 不改 gate 逻辑，不改 pr-create-guarded 代码
- residual_risk: 新增 gate 规则时需要同步更新 skill 模板
