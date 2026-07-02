---
candidate_id: C-20260701T085407Z-A
status: absorbed
source_raw: raw-20260701T085407Z
created_at: 2026-07-01
milestone: M-20260701T085407Z-A
---

## C-20260701T085407Z-A: A2A reviewer restore + routing + session

- candidate_format_version: v2
- title: A2A reviewer agent — ACP/A2A 集成 + session/fork 复用 + agent_working 表
- status: absorbed
- decision_reason: 工作直接在 raw issue 上完成（94 commits），涵盖 ACP session 管理、A2A SSE 路由、agent_working 表、双看门狗、session/fork 缓存复用、InputRequiredReason 12值枚举、三 loop Reviewer 集成。无需独立 I-* issue——所有实现在 fix 分支内完成。
- next_action: N/A（已 absorb 到 raw issue）
- revisit_trigger: N/A（已 absorb）
- acceptance_criteria:
  - ACP bridge session/resume 透传 prompt
  - watchdog session/prompt 优先 + fork from Manager 决策树
  - agent_working 表: UPSERT(Worker) + UPDATE_ONLY(Reviewer) + __manager__ 自举
  - InputRequiredReason 12 值枚举 + 6 向路由
  - Reviewer dispatch: A2A SSE → watchdog → ACP session/fork → session/prompt
  - 82 tests GREEN
- promotion_gate: N/A（已 absorb）
- open_questions: []
- absorbed_into: raw-20260701T085407Z
- milestone: M-20260701T085407Z-A
- session_refs: []
