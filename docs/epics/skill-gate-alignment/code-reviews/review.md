# Code Review: skill gate alignment
- issue_id: I-20260508T011858Z-A
## Implementation Decision Note
- decision: 在三个 skill 中添加完整示例，删除冗余叙述
- why_this: 按示例写自然达标，无需门禁契约章节
- alternatives_considered: 门禁契约章节（拒绝：AI 会作弊迎合）
- boundary_non_goals: 不改门禁工具代码
- residual_risk: none

## Dev Continuation (2026-05-10)
- changes:
  - doc-B1: 移除冗余 "wt-create 已经准备好了。"
  - doc-B2: 移除冗余 "milestone 已经准备好了。"
  - dev-loop: 移除 "AI-native" (非标准限定词)；合并 three-loop 真源注记为一行
- pre-tests AT-001 verification: 三个 skill 示例完整、无冗余叙事
- verdict: all acceptance items pass
