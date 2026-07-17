---
issue_id: I-20260717T004752Z-A
issue_path: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T004752Z/issues/I-20260717T004752Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260717T004752Z-A
- issue_path: docs/B2-docs/runtime/application-native-runtime-observation-contract-and-observability-planes/raw-20260717T004752Z/issues/I-20260717T004752Z-A.md

## Implementation Decision Note

- decision: 文档批量对齐（heartbeat/bridge/task_mode/storm/Loop Guard/trace §11+§12/AGENTS 纠错）+ L240 打点一行修复
- why_this: 审计逐条坐实的真源漂移；L240 是契约自认必须补齐的缺口且下一跳有当日 trace 实证；L041/L042 涉 monitor 结构以 known-gaps 显式记录避免过度改动
- alternatives_considered: 只补文档不修 L240（契约继续自我违反，否）；连 L041/L042 重构（monitor 风险，独立 lane）
- boundary_non_goals: 不动 monitor；不改 SVG；不新增语义只镜像真源
- residual_risk: 文档与代码未来再漂移——trace §11 对照脚本（AT-001 harness）留档可复跑，可被后续 gate 吸收
