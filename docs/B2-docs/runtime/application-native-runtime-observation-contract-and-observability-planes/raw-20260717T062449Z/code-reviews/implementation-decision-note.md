---
issue_id: I-20260717T062449Z-A
issue_path: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T062449Z/issues/I-20260717T062449Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260717T062449Z-A
- issue_path: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T062449Z/issues/I-20260717T062449Z-A.md

## Implementation Decision Note

- decision: L041 前移至 child 首活确认；L042 原位 IN+六出口分支 OUT；cleanup 链条件出口；§12 同步
- why_this: in/out API 原生支持拆相；打印权归真正决策层（契约 §8）；零业务逻辑改动
- alternatives_considered: 事后推断 to（违反打印权归属，否）；monitor 全量重构（另案）
- boundary_non_goals: 不改路由/清理逻辑；接力型下游（L201/L210/L230/L240）的衔接由下游 IN 记录
- residual_risk: 出口分支若未来新增而漏打 OUT，将表现为 L042 只 IN 无 OUT（契约 §7 可判定断链）——比候选集假 OUT 更可发现
