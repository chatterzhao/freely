---
issue_id: I-20260625T084506Z-A
issue_path: docs/issues/I-20260625T084506Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260625T084506Z-A
- issue_path: docs/issues/I-20260625T084506Z-A/issue.md

## Implementation Decision Note

- decision: 在 B2_IBM SKILL.md 模板前内嵌反糊弄铁律警告 + pretests-retirement-gate 新增 E2E/集成测试层级硬拦截
- why_this: gate 层已有反作弊检查（#3451），但 skill 层缺少预防性指导。内嵌警告确保 AI 写 pre-tests.md 时必然看到。gate 层新增层级检查作为最后防线
- alternatives_considered: 考虑过单独创建反糊弄规范文档链接到 skill，但 AI 可能不读链接，内嵌更可靠
- boundary_non_goals: 不改 test-execution skill（由 #3495 单独负责）；不改 pretests-gate 二进制（fallback 路径已覆盖）
- residual_risk: 端到端验证需在后续真实 issue 的 pr-create-guarded 流程中触发，本次改动仅验证 gate 逻辑存在性
