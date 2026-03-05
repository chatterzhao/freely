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
- status: promoted
- decision_reason: 前后端解耦主线的关键前置，需先冻结最小 API 契约。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []

### C-20260304-202
- title: 多项目 UI 隔离规则实现
- problem: 交互语义已定义，未落地为实现任务。
- why_now: 会影响自治开发触发与观察体验。
- acceptance_hint: 实现 Focus/Overview、activeProject 高亮、项目级输入隔离。
- priority: P1
- status: promoted
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
- status: promoted
- decision_reason: 来自该研究核心结论与执行建议，属于减少返工的关键约束。
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
