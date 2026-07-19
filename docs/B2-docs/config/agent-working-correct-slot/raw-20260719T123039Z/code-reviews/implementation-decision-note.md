---
issue_id: I-20260719T123039Z-A
issue_path: docs/B2-docs/config/agent-working-correct-slot/raw-20260719T123039Z/issues/I-20260719T123039Z-A.md
phase_state: completed
---
- issue_id: I-20260719T123039Z-A
- issue_path: docs/B2-docs/config/agent-working-correct-slot/raw-20260719T123039Z/issues/I-20260719T123039Z-A.md
## Implementation Decision Note
- decision: cleanup stale agent_working行 + 真实DB验证测试
- why_this: Python/DB层正确, shell层已修, 旧数据存在 + 测试只grep代码不查DB
- alternatives_considered: (A)不改测试—GREEN但DB值仍错; (B)只cleanup不加测试—下次出问题无法发现
- boundary_non_goals: 不改agent_working逻辑; 不改agent-table.toml
- residual_risk: 无
