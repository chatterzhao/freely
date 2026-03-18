# Candidates - 20260318-1222--mem9-shared-memory-fit-for-freely

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260318-1222-01
- title: Evaluate mem9 as an optional continuity-plane backend for Freely
- problem: Freely 已有本地 continuity / recovery / session rotation，但缺少跨工具、跨机器的共享记忆候选评估。
- why_now: `mem9` 明确支持多种 AI coding agent，且方向与 Freely 的多工具未来形态有重叠。
- acceptance_hint: 明确 Freely 与 mem9 的边界，给出适合 materialize 的 issue 或 skill 方向。
- priority: P2
- status: needs_research
- decision_reason: 值得研究，但当前更像未来增强层，不应打断正在推进的主管/worker 主线。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs:
  - github:https://github.com/mem9-ai/mem9
