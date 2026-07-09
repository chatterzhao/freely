---
issue_id: I-20260709T232630Z-A
issue_path: docs/B2-docs/acp/bridge-lifecycle-management/raw-20260709T232630Z/issues/I-20260709T232630Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260709T232630Z-A

## Implementation Decision Note

- decision: `acp-bridge.log` → `acp-bridge-{base_tool}.log`，检测函数改用 glob 扫描所有 per-tool 日志
- why_this: 三个 bridge 共用单一日志导致 truncate 互相覆盖，per-tool 分离最简且每个 bridge 启动时 truncate 只影响自己
- alternatives_considered: 单一日志 + base_tool 前缀 — 仍会互相覆盖，truncate 问题未解决
- boundary_non_goals: 不改变日志格式和内容，只改文件路径
- residual_risk: 零
