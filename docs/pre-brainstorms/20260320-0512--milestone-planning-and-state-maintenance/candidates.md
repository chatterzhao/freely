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
- legacy_id_mapping: I-20260320-0512  # 历史遗留的 issue id
- milestone: `M-20260306-workspace-routing-foundation`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

### C-20260327-parked-worktree-retirement
- title: Milestone-coupled parked worktree retirement planning
- problem: 当前 Freely 已经能维护 milestone sequencing，也能做 worktree retirement handoff，但还没有一条显式能力说明：当某个 research / merge-prep worktree 的剩余动作只是在 milestone 中把远期 issue 排到后面时，应优先完成 milestone 写回并退休该 worktree，而不是把 worktree 长期保留为未来 queue 的占位符。
- why_now: 随着治理树、frontend probe 和多条 follow-on issue 同时存在，单靠“暂时还会再用到这棵树”会让 worktree fleet 越挂越多。Freely 需要把“近程 active batch”和“已排序但暂不执行的 parked issue”区分开，并让 milestone maintenance 与 worktree retirement 配套。
- acceptance_hint:
  - `milestone-planning-state-maintenance` 能明确输出 `active now` 与 `parked for later cost window`
  - `worktree-maintenance-governance` / cleanup handoff 能消费这个判断，允许“里程碑已写回，因此当前树可先 retire”
  - research / merge-prep worktree 不再因为 future queue 占位而被长期 retained
  - 重新进入被 parked issue 时，默认从 canonical `develop` 或最新上游新开 dedicated worktree，而不是依赖旧树长期存活
- priority: `P1`
- status: `needs_research`
- decision_reason: 这不是简单调整当前 milestone 排序，而是要把 milestone sequencing 与 worktree retirement 联动成 Freely 自维护能力；现有 `milestone-planning-state-maintenance` 与 `worktree-maintenance-governance` 已覆盖两端，但中间的“parked issue allows retirement”契约尚未显式冻结。
- promoted_issue_path: `pending://issue-materialization`
- milestone: `M-20260306-workspace-routing-foundation`
- next_action: 先收敛最小契约：哪些 milestone 证据足以支持 research worktree retirement，哪些 phase_state / queue ordering 可以表达 `parked but not active`，以及 manager 应如何把这个判断交给 cleanup / retirement handoff。
- revisit_trigger: 当某个 worktree 的剩余动作已退化为 milestone 排序维护，而不是近程 issue continuation 时重新唤起。
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]
