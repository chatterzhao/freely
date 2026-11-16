---
issue_id: I-20261116T050414Z-A
issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261116T050414Z/issues/I-20261116T050414Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20261116T050414Z-A
- issue_path: docs/B2-docs/platform/raw-replica-reconciliation/raw-20261116T050414Z/issues/I-20261116T050414Z-A.md

## Implementation Decision Note

- decision: 把标题规范化作为 `freely task-source-scan` 的独立 preflight（scan 唯一漏斗），pr-create 保留同类 preflight 覆盖 CLOSED/absorbed；gate 只增强只读诊断。
- why_this: 历史上 `pull_raw_issue()` 已能自动规范化但只挂物化路径，且被防重新物化守卫挡住 CLOSED raw；用户明确要求「从平台拿 raw 起就是标准标题」，scan 是唯一入口。把写放在命令编排层既不破坏 pre-scan/gate 的只读契约，也让所有下游任务受益。
- alternatives_considered: gate 内自愈（破坏 write-free receipt，否决）；只改 pull 守卫（重新物化 CLOSED raw，否决）；只靠 pr-create（太晚，降级为兜底）。
- boundary_non_goals: 不改 `canonical_raw_title()` / `_resolve_raw_identity()`；不放宽 ambiguous；不修 body/comments/labels/本地文档；不改 `pre-scan-fix.sh` 与 `task-lifecycle-scan.py` 分析器；不追溯历史 CLOSED raw 标题。
- residual_risk: 平台 raw 的 title 和 body 都不含 `raw-<key>` 时无法定 key，本轮跳过并告警（不猜 created_at）；单平台读失败时跳过该平台并留痕，不阻断 scan。
