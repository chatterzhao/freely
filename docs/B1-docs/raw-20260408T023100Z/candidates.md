# Candidates - 20260408-0231--runtime-concurrent-start-lock-and-status-surface-alignment

## Context

- Source brainstorm: `./brainstorms.md`
- Status: `active`
- Route: `research-to-bounded-repair`

## Candidates

### C-20260408T023100Z-A: legacy issue

- candidate_format_version: `v2`
- title: `Runtime concurrent start lock and generated status-surface alignment`
- research_only: `false`
- implementation_ready: `true`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_id: `I-20260408T023100Z-A`
- promoted_issue_path: `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/issues/runtime-concurrent-start-stop-followthrough-governance.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `none`
- problem: The original packet contained two defects. The `status` / `fleet-status` generated-truth half has already landed on `develop`, and the remaining runtime followthrough now has a bounded implementation in the active lane: same-project starts keep bootstrap-in-flight attach behavior under degraded inspection, `freely stop` terminates every discovered same-project supervisor, and stop-marker cleanup no longer lets leftover duplicate supervisors survive or accidentally pin the project in stop mode. The unresolved work is now canonical closeout truth, not another round of runtime design.
- why_now:
  - dogfood evidence on `2026-04-08 01:23:58 PDT` showed three same-second supervisors for one worker project
  - stopping that worker required hard-kill fallback, so the defect is operationally harmful rather than cosmetic
  - commit `3ef222ec` already absorbed the status-surface half on `develop`, so the remaining worktree should now be judged only on the runtime followthrough still missing from canonical truth
  - current implementation evidence in `feature/runtime-concurrent-start-stop-fix-20260410` now covers the attach/stop followthrough and focused regressions, so the lane needs canonical closeout writeback rather than another round of broad research
- acceptance_criteria:
  - concurrent same-project `freely start --project` calls materialize at most one `supervisor_started` runtime event
  - later concurrent callers either attach/reuse or exit after bounded wait; they do not create a second supervisor
  - stale start-lock recovery is bounded and does not block future starts forever
  - degraded process inspection keeps the hinted same-project supervisor alive while bootstrap grace is still active; it does not tear the supervisor down before attach/reuse can happen
  - `freely stop --project` terminates all discovered same-project supervisors, including supervisors not currently recorded in `supervisor.pid`
  - stop-marker cleanup only clears the marker when no other same-project supervisor remains alive
  - focused regression tests cover the already-landed generated-truth repair plus the remaining attach/stop followthrough
- promotion_gate:
  - keep the repair inside runtime start serialization and same-project supervisor cleanup
  - do not widen into broader worker recovery policy, semantic-loop policy, or provenance research
  - preserve the already-landed baseline/fleet generated-truth behavior where `generated != consumed` is allowed
- open_questions:
  - should the remaining runtime followthrough stay as a continuation of `C-20260408T023100Z-A`, or be split into a new bounded owner once the current worktree writes canonical issue truth
  - do we need any extra replay beyond focused script tests to prove the stop-marker preservation does not regress normal single-supervisor stop behavior
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author-review`
    summary: `The original packet was valid, but one half is now already on develop. The unfinished part is the runtime followthrough around attach/stop cleanup for same-project duplicate supervisors, and it remains narrow enough to repair without reopening broader governance families.`
    verdict: `ready_for_bounded_repair`
- next_action: Execute `I-20260408T023100Z-A` as the bounded followthrough owner for the remaining same-project start/stop repair. Keep the generated-truth half closed on canonical `develop`, carry only the focused runtime start/attach/stop evidence, and promote through a guarded merge chain.
- revisit_trigger: Reopen only if the lock-based repair still allows duplicate same-project supervisors, if degraded bootstrap attach still tears down a healthy in-flight supervisor, or if the stop-marker cleanup keeps a stopped project falsely pinned after the last supervisor exits.
- decision_reason: `This remains a bounded runtime correctness packet. The status-surface subproblem was already absorbed on develop, leaving a still-narrow attach/stop followthrough that belongs with the same same-project duplicate-supervisor evidence family rather than a new architecture track.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
