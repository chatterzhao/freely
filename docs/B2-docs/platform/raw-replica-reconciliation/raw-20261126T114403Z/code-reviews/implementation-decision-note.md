---
issue_id: I-20261126T114403Z-A
issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261126T114403Z/issues/I-20261126T114403Z-A.md
phase_state: done_b2_ibm
---

# Implementation Decision Note

- issue_id: I-20261126T114403Z-A
- issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261126T114403Z/issues/I-20261126T114403Z-A.md
- decision: adapter 增批量子命令 `close-local-ids`，一次读取 open records 后复用同一判据关闭所有 terminal id；命令层只枚举 id 与汇总。
- why_this: `platform-adapter.py:1308` 明确副本判据归 adapter；命令层自己拼 ids 会产生第二套语义与部分成功回执（R60.2 同类 bug）。
- alternatives_considered: 命令层缓存 records 循环调用单 id CLI（跨进程缓存失效，仍需改 adapter）；daemon 常驻 records 缓存（超出本轮边界，留 revisit_trigger）。
- boundary_non_goals: 不改单 id 入口；不改本地 frontmatter；不放宽终态判据；不新增平台写通道。
- residual_risk: 平台读取失败时批量整体 fail-closed，需重试整批；retry 命令按 id 打印，可接受。
