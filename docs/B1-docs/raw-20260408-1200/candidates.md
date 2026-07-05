# 候选：develop-push-followthrough-escalation

- id: `C-20260408-1200-A`
- candidate_format_version: `v2`
- title: Freeze develop push urgency and upstream-resync escalation after protected-branch merge
- source_brainstorm: `docs/B1-docs/raw-20260408-1200/brainstorms.md`
- problem: Freely already exposes `push_pending` / `push_deferred` after lawful `develop` merge, but it still lacks a canonical contract for when unresolved push debt must become the manager's first followthrough action and when active worktrees must absorb the latest `develop` before continuing owner judgment. Without that contract, local-only canonical truth can linger and stale worktrees can continue making governance decisions on outdated upstream state.
- why_now:
  - root `develop` is currently ahead of `origin/develop`, which proves the repo can remain in lawful-but-local-only followthrough state for a meaningful window
  - active research lanes can misclassify blockers when they do not absorb the latest `develop` before continuing
  - the completed first-slice owner intentionally stopped at visibility/defer truth and left stronger followthrough semantics for a new lifecycle
- acceptance_criteria:
  - define when `push_pending` must be treated as immediate followthrough rather than merely visible debt
  - define which defer reasons allow temporary continuation and which require manager escalation or stop-the-line behavior
  - define when an active feature/research worktree must merge/rebase latest `develop` before continuing doc-loop / verification / cleanup judgment
  - define the minimum patrol/status truth needed to surface `push urgency` and `resync required`
  - preserve the rule that hooks/runtime must not auto-push on behalf of the operator
- promotion_gate:
  - do not reopen `develop-push-pending-guard-governance`; treat this as the documented follow-on for stronger followthrough semantics
  - do not turn the first slice into hook auto-push or hidden network side effects
  - show that stale-upstream worktree judgment is a repeated governance gap, not a one-off operator mistake
- open_questions:
  - should `push urgency` become a new machine-readable state or remain a patrol-derived classification
  - should unresolved `push_pending` block only new protected-branch merges, or also new worker launches / new lanes
  - should `resync required` derive from base-sha drift, protected-branch merge count, or owner-visibility sensitivity
  - should this materialize as one owner or split into `push escalation` and `upstream resync trigger` owners
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The gap is no longer visibility of develop push debt. The missing next slice is urgency plus stale-upstream resync governance for active worktrees.`
    verdict: `ready_for_pre_brainstorm`
- priority: `P0`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_id: `I-20260408-1200-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/develop-push-followthrough-escalation-governance/issues/develop-push-followthrough-escalation-governance.md`
- decision_reason:
  - the repo already has canonical push-debt truth, so the next problem is sequencing, not state discovery
  - the repo has already demonstrated that stale research trees can continue on outdated assumptions until develop is re-absorbed
  - timely push matters because AI/runtime interruption can strand lawful merges locally, but auto-push remains the wrong mechanism
- next_action:
  - candidate mirror only. `I-20260408-1200-A` is now the canonical owner for develop push followthrough escalation governance
  - implementation should first freeze timely-push default, lawful defer, and resync trigger before widening into runtime enforcement
- revisit_trigger:
  - another protected-branch followthrough round leaves `develop` ahead of remote without a stronger prioritization contract
  - another active worktree continues owner/blocker judgment on stale upstream truth and only later discovers the gap after resync
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
