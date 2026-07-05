# Candidates: 里程碑状态标识符语义收敛

## C-20260308-1501

- title: 里程碑状态标识符重命名与职责边界收紧
- status: dropped
- decision_reason: 该候选只覆盖“改名与职责边界收紧”，后续被 `C-20260308-1631` 的阶段前缀式主进度标识方案吸收并替代；继续单独推进会造成并行状态主线。
- promoted_issue_path: `docs/epics/workspace-routing-foundation/stage-prefixed-progress-identifier/issues/stage-prefixed-progress-identifier.md`
- milestone: `docs/milestones.md#m-20260306-workspace-routing-foundation`
- acceptance_hint: 本候选不再单独 materialize；后续统一以 `phase_state` 词典、`done_ibm` handoff 和恢复边界治理作为正式实现口径。
- superseded_by:
  - `docs/B1-docs/raw-20260308-1630/candidates.md#c-20260308-1631`
  - `docs/epics/workspace-routing-foundation/stage-prefixed-progress-identifier/issues/stage-prefixed-progress-identifier.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "analysis"}]
- scope:
  - LAWS 2C 流程标识词典
  - milestones.md milestone_state_policy
  - 所有 docs/epics/**/issues/*.md 状态字段
  - 相关 skills 状态判断逻辑
- impact: 中等 - 需要更新多个文档，但语法层面兼容（只是值域变化）
