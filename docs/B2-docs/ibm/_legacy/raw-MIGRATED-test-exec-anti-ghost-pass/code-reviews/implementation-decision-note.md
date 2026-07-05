---
issue_id: I-20260625T084522Z-A
issue_path: docs/issues/I-20260625T084522Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260625T084522Z-A
- issue_path: docs/issues/I-20260625T084522Z-A/issue.md

## Implementation Decision Note

- decision: 在 test-execution SKILL.md 增加步骤 4（可执行性检查），执行前拦截糊弄测试方案
- why_this: 执行端拦截比 gate 更早，与 B2_IBM 反糊弄铁律 + pretests-retirement-gate 形成三道防线
- alternatives_considered: 完全依赖 gate → 用户到 pr-create 才发现，浪费时间
- boundary_non_goals: 不改 pretests-retirement-gate（#3494）、B2_IBM skill（#3494）
- residual_risk: E2E 验证需后续真实 issue 触发
