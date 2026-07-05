---
issue_id: I-20260625T153111Z-A
issue_path: docs/issues/I-20260625T153111Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260625T153111Z-A
- issue_path: docs/issues/I-20260625T153111Z-A/issue.md

## Implementation Decision Note

- decision: 新建 .freely/agent-table.toml（TOML 格式）+ bin/agent-table-query（Python 解析器），集成到 sync_project_tooling_from_source
- why_this: TOML 是 config.toml 同格式，Python 解析器可被 shell 调用，sync_tooling 是已有集成点无需新 hook
- alternatives_considered: 嵌入 config.toml → 字段冲突；JSON → 手写不友好
- boundary_non_goals: 不改 Manager patrol 调度逻辑（后续独立 PR）；不实现锁机制
- residual_risk: 当前只分配第一个 worker slot，未实现真正的空闲检测和多 worker 并发分配
