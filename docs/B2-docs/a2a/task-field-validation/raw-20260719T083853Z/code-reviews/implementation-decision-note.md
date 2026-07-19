---
issue_id: I-20260719T083853Z-A
issue_path: docs/B2-docs/a2a/task-field-validation/raw-20260719T083853Z/issues/I-20260719T083853Z-A.md
phase_state: completed
---

- issue_id: I-20260719T083853Z-A
- issue_path: docs/B2-docs/a2a/task-field-validation/raw-20260719T083853Z/issues/I-20260719T083853Z-A.md

## Implementation Decision Note
- decision: L1(a2a_task handler) + L2(DB insert) + L3(agent_assign) 三层校验 + prompt模板补全
- why_this: 当前写入链三层全通零拦截, worktree/branch/raw-key空值静默写入DB
- alternatives_considered: (A) 只修prompt模板 — AI仍可能传错; (B) 只加L1 — 其他调用路径无保护
- boundary_non_goals: 不改DB schema(NOT NULL migration独立issue); 不清理历史僵尸task
- residual_risk: 无
