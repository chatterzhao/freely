# Candidates - 20260319-1105--three-loop-capability-lifecycle-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260319-1105-A
- title: 三层循环能力映射、owner 边界与生命周期真源收敛
- problem: Freely 已有大量自治能力，但能力归属、调用边界和生命周期散落在多个高层文档与 skills 中，缺少唯一真源，长期维护会产生冲突和不同步。
- why_now: 这是 Freely 继续扩展 watchdog、continuity、supervision、milestone intake 等能力前的基础治理面；若不先收敛，后续只会继续长出更多平行口径。
- acceptance_hint: 新增一个自包含的三层循环能力与生命周期真源文档；明确 capability -> loop -> owner -> artifact -> transition 映射；把 `CONSTITUTION`、`PROJECT_INTENT` 和关键 skills 收紧为摘要加引用。
- priority: P0
- status: needs_research
- decision_reason: 边界已经足够稳定，且唯一细节真源与全量能力 inventory 已初步落盘；下一步重点不是重新讨论三层循环本身，而是检查剩余未决边界是否需要继续 materialize 成独立 IBM issue。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
