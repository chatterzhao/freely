---
candidate_id: C-20260701T045911Z-A
status: needs_research
source_raw: raw-20260701T045911Z
created_at: 2026-07-01
milestone: M-20260701T045911Z-A
---

## C-20260701T045911Z-A: Reviewer agent + per-step workflow 介入

- candidate_format_version: v2
- title: Reviewer 成为独立 agent，workflow 每步经过 reviewer 审查
- status: needs_research
- decision_reason: 7 个已有组件研究完成。4 个 Phase 待拆分推进。
- next_action: 拆分 Phase 1（Reviewer 独立 agent）为子 candidate，先实现基础 reviewer 生命周期
- revisit_trigger: Phase 1 完成后评估是否需要拆 Phase 2-4
- acceptance_criteria:
  - Phase 1: Reviewer 作为独立 ACP agent 启动，A2A task 支持 reviewer role
  - Phase 2: Workflow 每步设 input-required → reviewer 介入
  - Phase 3: SSE 实时路由替代轮询
  - Phase 4: Worker pool N>1 并发
- promotion_gate: Phase 1 reviewer 能接收 A2A task 并产出审查结论
- open_questions:
  - Reviewer slot 是否独立于 worker？（建议独立，避免 rate-limit 竞争）
  - Reviewer 运行在 develop worktree（复用 Manager）还是独立 worktree？
  - Reviewer guidance 回写机制：A2A message / 文件 / SSE？
  - 审查结论格式：结构化 JSON 还是自然语言？
  - 每步介入还是关键步骤（B1/B2/pr-*）？
  - 是否需要 `[reviewer]` next_action 路由？
- review_conclusion: |
    B1 审查通过。7 组件分析准确，6 缺口确认，4 补充点已加入 brainstorms。
    Phase 1 scope 明确：ensure_reviewer() + A2A reviewer role + [reviewer]路由。
    建议拆 C-20260701T045911Z-A 为子 candidate 逐 Phase 推进。
- promoted_issue_id: (待拆分为子 candidate)
- milestone: M-20260701T045911Z-A
- session_refs: []
