# Candidates - 20260319-1105--three-loop-capability-lifecycle-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260319-1105-A
- title: 三层循环能力映射、owner 边界与生命周期真源收敛
- problem: Freely 已有大量自治能力，但能力归属、调用边界和生命周期散落在多个高层文档与 skills 中，缺少唯一真源，长期维护会产生冲突和不同步；同时“`三层`”这一中文口径也开始把 `auto-loop / doc-loop / dev-loop` 误导成包含关系，进一步污染 owner 与 transition 判断。
- why_now: 这是 Freely 继续扩展 watchdog、continuity、supervision、milestone intake 等能力前的基础治理面；若不先收敛，后续只会继续长出更多平行口径，并让 `doc-loop` / `dev-loop` / verification / cleanup 的关系持续被误读。
- acceptance_hint:
  - 新增或收紧一个自包含的三个 loop 能力与生命周期真源文档
  - 明确 `auto-loop` 与 `doc-loop` / `dev-loop` 的并列关系，不再让“层级”词面暗示包含
  - 明确 capability -> loop -> owner -> artifact -> transition 映射
  - 先完成 active truth / active lifecycle / historical evidence 的分层审计，再决定真源改写范围
  - 把 `CONSTITUTION`、`PROJECT_INTENT` 和关键 skills 收紧为摘要加引用
- priority: P0
- status: needs_research
- decision_reason: 唯一细节真源与全量能力 inventory 已初步落盘，但“三个 loop 的并列关系”和“何处必须改词、何处只保留历史证据”这两层边界仍未完全收稳。下一步重点不是新开平行 candidate，而是吸收 `20260323-0241` continuation，完成 active truth 审计与 sibling-loop 关系纠偏，再决定是否需要继续 materialize 成独立 IBM issue。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
