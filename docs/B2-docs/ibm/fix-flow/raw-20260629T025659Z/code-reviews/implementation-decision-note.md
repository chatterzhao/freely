---
issue_id: I-20260629T025659Z-A
issue_path: docs/B2-docs/ibm/fix-flow/raw-20260629T025659Z/issues/I-20260629T025659Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260629T025659Z-A
- issue_path: docs/B2-docs/ibm/fix-flow/raw-20260629T025659Z/issues/I-20260629T025659Z-A.md

## Implementation Decision Note

- decision: 统一 fix 和 feature skill 的 IBM 治理顺序为 B1→B2→dev→test。fix 的 B1/B2 是轻量版——结构相同但分析深度不同
- why_this: 治理文档在开发之前才能真正保证质量。pre-tests 先于代码让 TDD 的 RED-GREEN 循环可以执行。统一流程降低认知负担
- alternatives_considered: (1) 保持 fix 治理后置 — 导致 pre-tests 走过场；(2) 按复杂度分级 — 引入主观判断，门禁无法区分
- boundary_non_goals: 不改变 hotfix 路径（仍可跳过 test-pre-merge）；不改变 B1/B2 skill 的核心模板；不合并 fix 和 feature 为一个 skill
- residual_risk: 简单 fix 也需要写 B1/B2 文档，可能降低极简修复的速度。通过 fix B1/B2 的轻量化设计缓解
