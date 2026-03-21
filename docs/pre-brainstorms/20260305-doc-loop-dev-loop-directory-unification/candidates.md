# Candidates - 20260305-doc-loop-dev-loop-directory-unification

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260305-801
- title: 目录迁移契约（Doc-Loop Contract）
- problem: 目标目录结构有定义，但缺少阶段化迁移契约与切流条件。
- why_now: 不先定契约会导致文档与脚本反复打架。
- acceptance_hint: 明确 Phase A-D、目录创建时机、旧目录退役条件、回滚条件。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: 目录迁移契约已被当前 canonical 目录模型取代，无需再补历史迁移 issue。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `AGENTS.md`
  - `docs/system/workspace/scripts/README.md`
- session_refs: []

### C-20260305-802
- title: 文档门禁对齐到新目录
- problem: `doctor/governance-check/hooks` 仍存在旧结构依赖。
- why_now: 若门禁不切换，目录重构无法真正生效。
- acceptance_hint: 将必检路径与规则改为 `pre-brainstorms + epics/progress/milestones` 新模型。
- priority: P0
- status: dropped
- adoption_type: superseded
- decision_reason: 门禁已经对齐到当前目录真源与 hooks/scripts 结构，不需要再单独 materialize。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
  - `docs/system/workspace/hooks/README.md`
- session_refs: []

### C-20260305-803
- title: Deferred 资产选择性迁移执行器
- problem: 已完成 deferred 工作区清理，但未来仍需按新模型选择性重建必要资产。
- why_now: 用于后续按需迁移，而非继续保留旧目录负债。
- acceptance_hint: 基于 issue 需要逐项迁移并补全新目录引用。
- priority: P1
- status: needs_research
- decision_reason: 旧目录已清理，后续迁移策略改为按需重建。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
