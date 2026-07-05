---
issue_id: I-20260626T161720Z-A
issue_path: docs/issues/I-20260626T161720Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260626T161720Z-A
- issue_path: docs/issues/I-20260626T161720Z-A/issue.md

## Implementation Decision Note

- decision: load_config 从 agent-table 解析 AGENT_AI_TOOL → 派生 AI_TOOL。删除所有 AI_TOOL 降级和 config 回写。freely init 生成 agent-table.toml 模板。
- why_this: AI_TOOL alias 残留（kiro-cli）导致 Manager 无法启动。agent-table 已正确定义 per-agent slot，应成为唯一真相源。
- alternatives_considered: 只修降级链（治标），config 写入绕路（多余），保持现状（bug 持续）
- boundary_non_goals: 不改 AI_TOOL_ADAPTER/CAPABILITIES/POLICY（独立配置项），不改 write_config 初始模板（向后兼容）
- residual_risk: 现有 112 处 $AI_TOOL 引用现在全部从 AGENT_AI_TOOL 派生，需验证无遗漏降级路径
