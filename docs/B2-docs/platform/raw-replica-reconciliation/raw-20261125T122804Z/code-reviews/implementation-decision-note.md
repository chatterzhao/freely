---
issue_id: I-20261125T122804Z-A
issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261125T122804Z/issues/I-20261125T122804Z-A.md
phase_state: completed
---

# Implementation Decision Note
- issue_id: I-20261125T122804Z-A
- issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261125T122804Z/issues/I-20261125T122804Z-A.md
- decision: 在 `raw_reconciliation._body()` 把生成型 `| updated |` 行归一化为占位值，其余正文与表格行保持严格比较。
- why_this: 该行是 frontmatter `updated_at` 的投影，有 4 个合法写入者且无一方回写本地表格；改判据对象才能根治，而不是逐个补写入者。
- alternatives_considered: `issue-sync update` 回写本地表格——只覆盖一个入口且只读命令产生本地写；排除整个表格——会掩盖 phase_state/created 真实分歧。
- boundary_non_goals: 不改 `platform_body()` 其他字段；不改平台写通道；不覆盖其他表格行的分歧。
- residual_risk: `| updated |` 行本身缺失或格式异常时不会被归一化，仍按原文比较（fail-closed）。
