# Candidates - 20260304-architecture-backend-first-and-frontend-decoupling

## Context
- Source brainstorm: ./brainstorms.md
- Status: reviewed

## Candidates

### C-20260304-201
- title: Backend API 契约冻结 v1
- problem: 前后端解耦已达共识，但接口尚未冻结。
- why_now: 不冻结接口会导致前端高返工。
- acceptance_hint: 明确 sessions/memory/commands/status 最小 API 集。
- priority: P0
- status: superseded
- decision_reason: 后续正式 issue 已承接该 API 契约冻结方向，不应继续保留为假 promotion 候选。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-backend-boundary-contract-v1-for-frontend-probe/issues/frontend-backend-boundary-contract-v1-for-frontend-probe.md`
- session_refs: []

### C-20260304-202
- title: 多项目 UI 隔离规则实现
- problem: 交互语义已定义，未落地为实现任务。
- why_now: 会影响自治开发触发与观察体验。
- acceptance_hint: 实现 Focus/Overview、activeProject 高亮、项目级输入隔离。
- priority: P1
- status: proposed
- decision_reason: 与多项目隔离交互主线一致，已形成明确实现边界。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

### C-20260304-203
- title: 先后端后前端执行门禁
- problem: 路线虽已结论化，但缺少可执行的阶段门禁，容易再次前后端并行返工。
- why_now: 研究明确了“后端闭环优先”，需固化为执行规则。
- acceptance_hint: 定义前端启动前必须通过的后端能力清单与验收门槛。
- priority: P0
- status: superseded
- decision_reason: “先后端后前端” 已被后续增量 dogfooding gate issue 明确吸收。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- superseded_by:
  - `docs/epics/frontend-probe-dogfooding-loop/incremental-dogfooding-gate-for-backend-increments/issues/incremental-dogfooding-gate-for-backend-increments.md`
- session_refs: []
