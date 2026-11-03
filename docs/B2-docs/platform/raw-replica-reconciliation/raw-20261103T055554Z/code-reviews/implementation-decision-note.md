---
issue_id: I-20261103T055554Z-A
issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261103T055554Z/issues/I-20261103T055554Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20261103T055554Z-A
- issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261103T055554Z/issues/I-20261103T055554Z-A.md

## Implementation Decision Note

- decision: 在 platform-adapter 增加纯函数 `_resolve_raw_identity`，按 `[RAW-{key}]` 标题前缀优先解析身份；`_discover_one` 与 `_unique_raw_issue` 统一改用它。
- why_this: 身份声明在标题前缀，body 引用是噪音；把规则收敛到单一纯函数可单测、避免多处漂移，并保持多真实身份 fail-closed。
- alternatives_considered: 只搜标题（丢历史兜底）；在调用方各自过滤（规则重复、漂移）；reconcile 侧忽略 ambiguous（破坏 fail-closed）。
- boundary_non_goals: 不改 reconcile/scan 消费逻辑；不改 issue 文本格式；不回写历史 issue。
- residual_risk: 平台标题若不符合 `[RAW-key]` 约定，会走单条兜底；多条真实身份仍 ambiguous，需要人工清理。
