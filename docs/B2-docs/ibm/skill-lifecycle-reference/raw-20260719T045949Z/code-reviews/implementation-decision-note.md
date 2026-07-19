---
issue_id: I-20260719T045949Z-A
issue_path: docs/B2-docs/ibm/skill-lifecycle-reference/raw-20260719T045949Z/issues/I-20260719T045949Z-A.md
phase_state: in_verification
---

- issue_id: I-20260719T045949Z-A

## Implementation Decision Note

- decision: 在三环生命周期文档中明确 test/review 为每个环的回环驱动力，而非独立层；同时更新 B1/B2 skill 交叉引用
- why_this: 原三环模型将 test 和 review 淹没在 auto-loop 的 gate 序列中，reviewer agent 虽然在 Layer 3 有定义但在三环架构表中没有显式位置。test 和 review 实际上是每个环的反馈机制——不通过就回环重走，这才是"环"的本意
- alternatives_considered: (A) 不修改三环模型，只在 B1/B2 skill 加链接 — 治标不治本，模型本身就是不完整的；(B) 新增独立 test-loop 和 review-loop — 过度设计，test/review 不是独立 workflow surface，而是嵌入每个环的反馈机制
- boundary_non_goals: 不修改 auto-loop gate 序列（test/review 的调度入口不变）；不修改 Reviewer Agent 的角色定义；不修改 SVG 图
- residual_risk: 无。文本文档修改，语义更精确，无运行时影响
