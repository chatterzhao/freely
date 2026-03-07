# Candidates - 20260307-0930--source-routing-and-derived-worktree-governance

## Context
- Source brainstorm: ./brainstorms.md
- Status: in_review

## Candidates

### C-20260307-1201
- title: 源分类、milestone-owned issue 与派生 worktree 路由治理
- problem: 当前对“哪些地方发现新问题”“里程碑是否能直接执行”“IBM 的 issue 来源”“progress 跟踪什么”“未合并父分支上的从属 issue 应从哪里创建 worktree”仍缺统一执行口径，导致 AI 容易只记住约束却不会在对的时机执行。
- why_now: Freely 作为自治系统，必须先把路由与 workspace 准备动作写成标准步骤，才能稳定吃自己的狗粮。
- acceptance_hint: 1) 将问题来源拆成原始发现源 / 编排来源 / 延续来源；2) 明确 candidate 必须先入 milestone，IBM 的 `I` 来自 milestone 已接纳 issue；3) 明确 `progress` 只跟踪 dev-loop；4) 将核心 skills 改成情景驱动步骤；5) 为 worktree 创建补充 `execution_base` / `integration_target` / `depends_on` 口径，并提供标准创建入口。
- priority: P0
- status: promoted
- decision_reason: 这是当前自治可靠性的结构性缺口；如果不先收敛，AI 在多 worktree / 多 agent 条件下会继续漏掉正确的前置动作。
- promoted_issue_path: `docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/issues/source-routing-and-derived-worktree-governance.md`
- milestone: docs/milestones.md#m-20260306-workspace-routing-foundation
- session_refs: []
