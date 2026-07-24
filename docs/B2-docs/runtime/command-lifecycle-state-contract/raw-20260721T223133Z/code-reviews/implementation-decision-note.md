---
issue_id: I-20260721T223133Z-A
issue_path: docs/B2-docs/runtime/command-lifecycle-state-contract/raw-20260721T223133Z/issues/I-20260721T223133Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260721T223133Z-A
- issue_path: docs/B2-docs/runtime/command-lifecycle-state-contract/raw-20260721T223133Z/issues/I-20260721T223133Z-A.md

## Implementation Decision Note

- decision: 将 raw metadata 合同与 PR 平台状态规划拆成两个独立模块；生命周期命令只按 `observe → normalize → validate → plan → effect → commit → aggregate` 编排，并保留各历史命令既有职责。raw v1 固定为 21 个有序字段：创建时一次初始化，后续仅改值；promotion 保留两阶段与 1:N children，`wt-close` 对治理 metadata 零写入。
- why_this: 两类缺陷都来自命令在状态未完整观测时直接迁移，但 raw schema 与 PR remote state 是不同领域。共享编排范式、隔离领域模型，能避免规则继续扩散到超大 runtime 和多个 Shell 入口。
- alternatives_considered: 仅删除 wt-create absorbed 写入不能修复消费者漂移；批量迁移历史 raw 风险过高；把全部规则写回 runtime 单体违反已知模块化债务约束；允许任一平台成功会产生平台分叉。
- boundary_non_goals: 不批量重写历史 raw；不恢复 feedback 在 develop 的本地写入；不让 wt-close 改 metadata；不把 linked `I-*` 的 `completed` phase 引入 raw；不引入无 writer/reader 证据的 `closed_at`、`closeout_reason`、`force_closed_*`；不改变真正 merge 的远端 head equality；不提供 raw git/gh 绕过。
- residual_risk: 历史 raw 的不完整 absorption 仍需 normalized reader 在危险操作中 fail closed；多平台执行阶段无法跨远端实现真正事务回滚，因此必须先全量观测并保留逐平台结果；真实 existing-PR 更新只能在 guarded merge 后通过暂停 continuation 验收。
