---
issue_id: I-20260719T074532Z-A
issue_path: docs/B2-docs/a2a/agent-instance-id/raw-20260719T074532Z/issues/I-20260719T074532Z-A.md
phase_state: in_b2_ibm
---

- issue_id: I-20260719T074532Z-A

## Implementation Decision Note

- decision: 接上 shell 层 5 个断点, 使 DB/Python 层已有的 agent 实例分配机制生效
- why_this: DB(next_free/upsert)和 Python(agent_working.py)已正确实现, 断点在 shell 层两条 launch 路径 + a2a_task + Runtime 发现 + prompt 模板。修复这些断点即可让整条链路工作
- alternatives_considered: (A) 重构为单一 launch 路径 — scope 过大, 风险高; (B) 只修一条路径 — 另一条仍然断链
- boundary_non_goals: 不改 agent-table.toml 格式; 不改 DB schema; 不改 Python agent_working.py; 不改 ACP bridge 逻辑
- residual_risk: 修复后需 daemon 重启验证; prompt 模板修改需要 Manager AI 下一轮 patrol 才能观察到效果
