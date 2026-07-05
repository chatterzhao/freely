---
issue_id: I-20260705T024320Z-A
issue_path: docs/B2-docs/config/agent-table/raw-20260705T024320Z20Z/issues/I-20260705T024320Z-A.md
phase_state: done_b2_ibm
---
- issue_id: I-20260705T024320Z-A
## Implementation Decision Note
- decision: 6 个 bug 全部为参数遗漏——需 base_tool/slot 处补传参数或从 agent-table 查询
- why_this: 全局 AGENT_AI_TOOL 在单 tool 场景正确，多 tool 场景需按 agent 区分
- alternatives_considered: 删除 AGENT_AI_TOOL 全面改为 agent-table 查询 → 改动面过大
- boundary_non_goals: 不改变 session fork 的跨 slot 继承（需 ACP 协议支持）
- residual_risk: 同 base_tool 不同 slot 的 fork 仍用 bridge slot 凭据，记录为已知限制
