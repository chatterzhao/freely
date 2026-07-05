# Candidates - 20260319-1105--three-loop-capability-lifecycle-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260319-1105-A
- title: 三个 loop 的能力映射、owner 边界与生命周期真源收敛
- problem: Freely 已有大量自治能力，但能力归属、调用边界和生命周期散落在多个高层文档与 skills 中，缺少唯一真源，长期维护会产生冲突和不同步；同时“`三层`”这一中文口径也开始把 `auto-loop / doc-loop / dev-loop` 误导成包含关系，进一步污染 owner 与 transition 判断。
- why_now: 这是 Freely 继续扩展 watchdog、continuity、supervision、milestone intake 等能力前的基础治理面；若不先收敛，后续只会继续长出更多平行口径，并让 `doc-loop` / `dev-loop` / verification / cleanup 的关系持续被误读。
- acceptance_hint:
  - 新增或收紧一个自包含的三个 loop 能力与生命周期真源文档
  - 明确 `auto-loop` 与 `doc-loop` / `dev-loop` 的并列关系，不再让“层级”词面暗示包含
  - 明确 capability -> loop -> owner -> artifact -> transition 映射
  - 先完成 active truth / active lifecycle / historical evidence 的分层审计，再决定真源改写范围
  - 把 `CONSTITUTION`、`PROJECT_INTENT` 和关键 skills 收紧为摘要加引用
- priority: P0
- status: promoted
- decision_reason: active truth 审计已经证明现有高层真源仍会把 `auto-loop / doc-loop / dev-loop` 渲染成“`三层`”或接近包含关系，且 terminal / verification / cleanup 的定位持续漂移；当前已足够 materialize 为独立 IBM+dev issue，用 active truth 改写纠正 sibling-loop 关系，再把历史 evidence 保持为历史。
- promoted_issue_path: `docs/B2-docs/ibm/three-loops-sibling-relationship-and-terminal-governance/issues/three-loops-sibling-relationship-and-terminal-governance.md`
- legacy_id_mapping: I-20260324-0405  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
