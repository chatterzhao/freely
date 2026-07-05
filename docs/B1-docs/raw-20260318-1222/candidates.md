# Candidates - 20260318-1222--mem9-shared-memory-fit-for-freely

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260318-1222-A: legacy issue
- title: Evaluate mem9 as an optional continuity-plane backend for Freely
- problem: Freely 已有本地 continuity / recovery / session rotation，但缺少跨工具、跨机器的共享记忆候选评估。
- why_now: `mem9` 明确支持多种 AI coding agent，且方向与 Freely 的多工具未来形态有重叠。
- acceptance_hint: 明确 Freely 与 mem9 的边界，给出适合 materialize 的 issue 或 skill 方向。
- priority: P2
- status: promoted
- decision_reason: 研究结论已经稳定到可 materialize 的边界；mem9 适合被定义为可选连续性增强层，而不是治理真源。
- promoted_issue_path: `docs/B2-docs/ibm/mem9-continuity-bridge/issues/mem9-continuity-bridge.md`
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs:
  - github:https://github.com/mem9-ai/mem9
