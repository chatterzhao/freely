---
candidate_id: C-20260716T040152Z-A
status: absorbed
source_raw: raw-20260716T040152Z
created_at: 2026-07-16
milestone: M-20260716T040152Z-A
---

# Candidates

## C-20260716T040152Z-A: Agent 编排链路缺陷修复

- candidate_format_version: v2
- title: 修复 Agent 编排链路的 a2a-exit --reason 缺失、Reviewer 调度竞态、测试覆盖缺失
- status: absorbed
- decision_reason: 分阶段修复——先紧急修 Bug 1 (Reviewer 调度断裂)，再修 Bug 2-5 (竞态和静默失败)，最后补端到端测试。Phase 1 最小改动、最快恢复链路。
- next_action: B2_IBM 物化 Phase 1 的 I-* issue → 写 pre-tests → RED → dev → GREEN → PR
- revisit_trigger: N/A (已 promote)
- acceptance_criteria:
  - `a2a-exit --state input-required --reason "needs-review:b1"` 能正确设置 A2A task 的 reason 字段
  - `watchdog_sse.py` 收到 reason="needs-review:b1" 时能正确路由到 reviewer (needs_role="reviewer")
  - `watchdog_sse.py` 收到空 reason 时能正确路由到 manager (needs_role="manager")
  - `freely-cycle` 不再内联 reviewer 分配逻辑，统一走 watchdog_sse.py
  - `agent_assign(update_only=True)` 在行不存在时输出 stderr 警告日志
  - `bin/a2a-exit` 可作为独立命令调用
  - `a2a_task.py list` 的 `--status` 和 `--state` 参数行为一致
  - 端到端测试覆盖 Worker→Reviewer dispatch 链路
  - 所有现有测试通过
- promotion_gate: Phase 1 修复完成 + 测试全部通过 (包括新增测试)
- open_questions: []
- acceptance_reviews: []
- promoted_issue_id: I-20260716T040152Z-A
- promoted_issue_path: docs/B2-docs/agent-orchestration/agent-dispatch-fix/raw-20260716T040152Z/issues/I-20260716T040152Z-A.md
- milestone: M-20260716T040152Z-A
- session_refs: []
