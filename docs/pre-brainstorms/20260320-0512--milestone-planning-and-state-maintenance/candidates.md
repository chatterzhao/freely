# Candidates - 20260320-0512--milestone-planning-and-state-maintenance

## Context
- Source brainstorm: `./brainstorms.md`
- Status: `promoted`

## Candidates

### C-20260320-0512-A
- title: Milestone planning and state maintenance
- problem: Freely 已经把 `docs/milestones.md` 作为 standing source 和项目级编排入口，但还没有一个明确能力专门负责 milestone sequencing、candidate/committed/completed 队列维护，以及 candidate/issue/progress/recovery/cleanup 之间的状态 reconcile，导致这些工作长期靠业务 worker 顺手补写。
- why_now: 本轮已经把 manager、auto-loop、lifecycle 与专门 skill 中的 milestone planning / state maintenance worker 语义落盘。当前缺口不再是“是否需要这个能力”，而是正式 materialize 为 canonical issue，避免真源和 milestone 仍停在 `pending://...materialization`。
- acceptance_hint:
  - manager 能在 standing-source scan 后识别“这是 planning/state-maintenance 问题”
  - `skill:milestone-planning-state-maintenance` 明确只做 sequencing / reconcile / writeback，不做业务实现
  - `three-loop-capability-lifecycle.md` 明确这是独立的 standing-source maintenance worker
  - `pre-brainstorm -> candidate -> milestone -> issue -> progress/recovery` 被视为需要同步收敛的治理事务
- priority: `P0`
- status: `promoted`
- decision_reason: manager 路由、auto-loop skill、专门 worker skill 与 lifecycle 真源都已改到位；继续把这条能力停留在 research 状态，会让 Freely 继续把 milestone maintenance 当成无 owner 的附属工作。
- promoted_issue_path: `docs/epics/workspace-routing-foundation/milestone-planning-and-state-maintenance/issues/milestone-planning-and-state-maintenance.md`
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]
