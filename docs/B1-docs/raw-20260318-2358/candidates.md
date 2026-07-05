# Candidates - 20260318-2358--manager-workcell-supervision-and-continuity

## Context
- Source brainstorm: ./brainstorms.md
- Status: in_research

## Candidates

### C-20260318-2358-A: legacy issue
- title: 项目级工位快照进入首跳 prompt 与 handoff
- problem: 当前主管会话没有项目级工位清单，只能看见总量，无法可靠排班。
- why_now: 这是主管工位真正可用的前置条件。
- acceptance_hint:
  - `wt-fleet-status` 输出按工位真实运行态取值
  - 首跳 prompt 注入项目级 fleet snapshot
  - handoff 附带项目级 fleet snapshot
- priority: P0
- status: absorbed
- decision_reason: `I-20260318-0930` 已以更早的 canonical owner `C-20260318-A` 承接 checkpoint / fleet / supervision 主线；当前候选只保留为同一 owner family 的后续 scope 输入，不再单独 materialize。
- promoted_issue_path: `docs/B2-docs/gate/checkpoint-commit-and-multi-worktree-supervision-governance/issues/checkpoint-commit-and-multi-worktree-supervision-governance.md`
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs: []

### C-20260318-2358-A: legacy issue
- title: lead-agent 与 auto-loop 的主管模式协议
- problem: 当前首跳协议只定义单工位路由，没有正式定义主管如何分配工位与委派 subagent。
- why_now: 如果协议层不落地，runtime 注入再多上下文也只是提示，不是 Freely 能力。
- acceptance_hint:
  - `lead-agent.md` 补主管职责
  - `auto-loop-orchestrator/SKILL.md` 补 manager-worker 模式
  - `multi-worktree-supervision/SKILL.md` 对齐主管工位工作流
- priority: P0
- status: absorbed
- decision_reason: `I-20260318-0930` 已吸收主管工位协议与多工位监督语义；当前候选不再需要独立 IBM owner，只作为该 canonical issue family 的补充来源保留。
- promoted_issue_path: `docs/B2-docs/gate/checkpoint-commit-and-multi-worktree-supervision-governance/issues/checkpoint-commit-and-multi-worktree-supervision-governance.md`
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs: []
