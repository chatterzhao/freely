# 候选：runtime-auth-repro

- id: `C-20260328-1856-A`
- title: Runtime auth repro and ownership classification follow-on
- source_brainstorm: `docs/pre-brainstorms/20260328-1856--runtime-auth-repro/brainstorms.md`
- status: `absorbed`
- adoption_type: `supporting_evidence`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `closeout-writeback`
- decision_reason:
  - branch-local evidence no longer supports a fresh auth/bootstrap owner boundary
  - the lane also stays outside the narrower active-worker delegated-continuation stall candidate because `pending_delegated_continuation_ids` never converged to that contract
  - the strongest surviving signal is broader continuity/control-plane drift around `resume_streak_limit`, `fresh_with_handoff`, `context compacted`, transport failure, and state-writeback reconciliation
  - that boundary is already better explained by the completed continuity/rotation contract than by any new auth/bootstrap or global-restart lifecycle
- why_now:
  - `feature/runtime-auth-repro-20260328-185604` is still dirty even though its committed branch tip is already merged to `develop`
  - without a canonical closeout, the stale lane keeps appearing as unresolved active work instead of same-family provenance
- expected_outcome:
  - classify the branch-local repro as supporting evidence only
  - keep future continuity/control-plane work on canonical owner lines rather than reviving this stale auth-named lane
  - make the worktree retirement judgement explicit
- likely_truth_sources:
  - `docs/epics/workspace-routing-foundation/token-efficient-session-continuity-and-rotation-governance/issues/token-efficient-session-continuity-and-rotation-governance.md`
  - `docs/progress/workspace-routing-foundation/p-token-efficient-session-continuity-and-rotation-governance.md`
  - `docs/epics/workspace-routing-foundation/live-status-current-runtime-state-reconciliation-governance/issues/live-status-current-runtime-state-reconciliation-governance.md`
  - branch-local runtime artifacts captured in `feature/runtime-auth-repro-20260328-185604`
- next_action:
  - do not materialize a new issue from this lane
  - treat the stale worktree as retirement-only provenance once cleanup notes are written back
- revisit_trigger:
  - only reopen as a new lifecycle if a future controlled repro isolates a missing auth/bootstrap contract that is not already explained by continuity/rotation or state-reconciliation owners
