---
issue_id: I-20261125T100958Z-A
issue_path: docs/B2-docs/acp/freely-host/raw-20261125T100958Z/issues/I-20261125T100958Z-A.md
phase_state: completed
---

- issue_id: I-20261125T100958Z-A
- issue_path: docs/B2-docs/acp/freely-host/raw-20261125T100958Z/issues/I-20261125T100958Z-A.md

# Implementation Decision Note
- decision: 缺本地文件时用 adapter search 按 raw key 发现 ids → update-issue；仅显式参数，不写本地文件。
- why_this: 与 cmd_comment 的纯平台语义一致；修改 raw 不需要实现它，不应耦合 wt-create。
- alternatives_considered: 要求 wt-create 先行——违背用户边界；回读平台 body——引入第二真源，否决。
- boundary_non_goals: 不改 create / wt-create / adapter 底层；保留既有本地文档场景行为。
- residual_risk: 平台 search 在历史重复副本场景可能多义，fail-closed 提示人工。
