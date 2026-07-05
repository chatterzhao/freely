# Candidates - 20260401-1831--worker-reactivation-reentry-residual-runtime-gaps

## Context

- Source brainstorm: `./brainstorms.md`
- Status: active

## Candidates

### C-20260401T183100Z-A: legacy issue
- candidate_format_version: v2
- title: Worker reactivation and local reentry residual runtime gap
- problem: completed workspace-routing owners still claim worker reactivation/reentry verification is closed, but current runtime evidence shows two residual gaps: worker chat/tui reactivation can still return optimistic `already_running_attach` without a durable `ai.pid`, and delegated continuation reentry still lacks a frozen canonical predicate for "active worker" on the worker side.
- why_now: these are the only remaining red tests after the autonomy-consent / project-local Codex config slice. Leaving them unowned would force the security lane to keep carrying unrelated runtime debt, and it would leave completed workspace-routing verification docs overstating closure.
- acceptance_criteria:
  - prove the exact worker-side attach-reuse path behind the current `test-freely-chat-worker-reactivation` failure
  - freeze the canonical worker-side local continuation reentry predicate and align the surviving test fixture or runtime behavior to it
  - ensure completed verification claims from `I-20260321T170600Z` and `I-20260322T041200Z` are either narrowed, superseded, or explicitly linked to the new follow-up owner
  - keep the repair scoped to worker reactivation/reentry semantics; do not widen into generic runtime orchestration redesign
- promotion_gate:
  - reproduce both failures in a focused workspace-routing lane
  - show why neither completed owner can absorb the residual without reopening scope beyond its frozen completion contract
  - name the narrower follow-up owner under `workspace-routing-foundation`
- open_questions:
  - should the follow-up split into two owners, or is one worker-runtime boundary issue still the smallest coherent slice
  - is the `test-freely-interruption-direct-answer` failure mostly a fixture truth problem, a runtime truth problem, or both
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `Both remaining failures sit on the worker-side runtime boundary rather than the current security lane. They are narrow enough to promote as one residual workspace-routing owner, with the first dev-loop task being to decide whether the second path needs runtime repair, fixture tightening, or both.`
    verdict: `promote`
- priority: P1
- status: promoted
- decision_reason: current evidence is sufficient to freeze one narrow follow-up owner under `workspace-routing-foundation`: both residuals sit on the same worker-runtime boundary and can share a first dev-loop step that resolves the surviving local-reentry ambiguity.
- promoted_issue_path: `docs/B2-docs/ibm/worker-reactivation-and-local-reentry-residual-runtime-governance/issues/worker-reactivation-and-local-reentry-residual-runtime-governance.md`
- next_action: finish issue-bound IBM closeout, then run a focused worker-runtime reproduction/repair slice under `I-20260401T183100Z-A`.
- milestone: `M-20260306-workspace-routing-foundation`
- revisit_trigger: if focused reproduction proves local reentry is purely stale fixture truth, narrow the implementation slice and update the issue/tasks rather than reopening candidate-level research.
- session_refs:
  - tool: `codex`
  - session_id: `current-thread`
  - jsonl_path: `unavailable://codex-thread-only`
  - role: `author`
