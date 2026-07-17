---
issue_id: I-20260717T090202Z-A
issue_path: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T090202Z/issues/I-20260717T090202Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260717T090202Z-A
- issue_path: docs/B2-docs/runtime/watchdog-restart-storm-and-process-churn-governance/raw-20260717T090202Z/issues/I-20260717T090202Z-A.md

## Implementation Decision Note

- decision: storm window tsv 增 kind 列，peak 仅对 death 行计，count 不变
- why_this: 恢复 churn 语义且保留观测面；回滚 10 使条件虚设
- alternatives_considered: PEAK 回 10（虚设，备选）；删条件（否）
- boundary_non_goals: 不动 count/WINDOW；不改原 lane 文件（GATE 1，勘误本 lane 引用）
- residual_risk: 旧 2 列行在 ≤120s 窗口内按 cycle 兼容，无死亡峰误判
