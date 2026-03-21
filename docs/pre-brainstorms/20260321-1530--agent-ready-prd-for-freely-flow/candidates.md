# Candidates - 20260321-1530--agent-ready-prd-for-freely-flow

## Context
- Source brainstorm: ./brainstorms.md
- Status: promoted

## Candidates

### C-20260321-1530-A
- title: Agent-ready PRD architecture for Freely IBM flow
- problem: Freely 当前的 `prd.md` 更偏“人类摘要”，还没有明确把 PRD 定义成 AI 时代的执行控制面。这会导致 AI 在 doc-loop 和 dev-loop 里只能拿到粗粒度目标，却缺 non-goals、task decomposition、prototype path、eval plan 和 model-upgrade revisit 触发器。
- why_now: 用户直接提出“在 IBM 流程里，AI 来出 PRD 应该长什么样”，且外部研究已经足以形成稳定判断；继续停留在抽象讨论，会让 Freely 自己的 doc-loop 仍沿用旧时代的 PRD 结构。
- acceptance_hint:
  - 明确 Freely 中 `B` 与 `PRD` 的边界：`B` 是 issue-bound brainstorm，`IBM` 整体才产出 `prd.md`
  - 给出 AI-ready PRD 的最小结构，而不是只复述“PRD 已死”
  - 把 PRD 定义成可以驱动 prototype、eval、task slicing 和 dev-loop 的控制面
  - 明确哪些字段属于稳定 contract，哪些字段需要随模型进展周期性重判
- priority: P0
- status: promoted
- decision_reason: 这轮研究已经从外部材料和 Freely 自身现状得出稳定结论：PRD 需要从“读物”变成“可执行包”。边界、产物、下一跳都已明确，足以进入正式 IBM issue。
- promoted_issue_path: docs/epics/ai-native-doc-loop/agent-ready-prd-for-freely-flow/issues/agent-ready-prd-for-freely-flow.md
- milestone: docs/milestones.md#m-20260321-ai-native-doc-loop
- session_refs:
  - tool: codex
  - session_id: current-thread
  - jsonl_path: unavailable://codex-thread-only
  - role: author
