# Candidates - 20260320-1410--worktree-maintenance-skill-taxonomy

## Context
- Source brainstorm: ./brainstorms.md
- Status: promoted

## Candidates

### C-20260320T141000Z-A: legacy issue
- title: Worktree maintenance governance skill
- problem: Freely 当前已有 branch/worktree 创建、checkpoint hygiene、multi-worktree supervision 和 premerge 能力，但缺“创建之后的维护能力”。这会让主管在处理大量 worktree 时只能反复临时拼接 milestone、issue、review、tests、git ancestry 和 companion/research 语义，导致多轮往返和重复判断。
- why_now: 本轮为了核清所有活跃 worktree 的真实状态，已经实际踩过 audit、merge-prep、retirement handoff 三类维护动作；边界已经稳定，值得固化成专门 skill。
- acceptance_hint:
  - 明确 `audit / merge_prep / retirement_handoff` 三种模式
  - 不重复 `branch-management` 的创建/cleanup 基础流程
  - 明确何时把 worktree 判成 `merge-ready / research-only / companion-only / retire-only`
  - 明确多树 merge-prep 时必须输出顺序、冲突面和回归门
  - 明确 historical / companion worktree 何时只能 salvage_then_retire
- priority: P0
- status: promoted
- decision_reason: 这次多轮 worktree 维护已经证明，该能力不再是抽象研究，而是 Freely 主管层的稳定日常动作；继续把它散落在 `branch-management`、聊天经验和 ad hoc 审计里，只会重复消耗轮次。
- promoted_issue_path: docs/B2-docs/ibm/_legacy-issues/raw-20260307-1201I-20260320T141000Z-A/issue.md
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
