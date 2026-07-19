---
issue_id: I-20260719T015321Z-A
issue_path: docs/B2-docs/agent-orchestration/agent-role-cleanup/raw-20260719T015321Z/issues/I-20260719T015321Z-A.md
phase_state: in_dev
---

- issue_id: I-20260719T015321Z-A

## Implementation Decision Note

- decision: 全项目清理 lead-agent.md 悬空引用，不恢复 lead-agent.md
- why_this: lead-agent.md 角色职责已被 manager-agent.md 吸收。恢复是回退，清理是前进。同步修复 governance-check 的落后 skill 路径（develop HEAD 已指向不存在的目录）
- alternatives_considered: (A) 恢复 lead-agent.md — 否决；(B) 只删 lead-agent.md 引用不修 skill 路径 — governance-check 仍 FAIL
- boundary_non_goals: 不恢复 lead-agent.md；不修改产品代码逻辑
- residual_risk: 无
