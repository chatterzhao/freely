# Candidates - 20260408-0231--runtime-concurrent-start-lock-and-status-surface-alignment

## Context

- Source brainstorm: `./brainstorms.md`
- Status: `active`
- Route: `research-to-bounded-repair`

## Candidates

### C-20260408-0231-A

- candidate_format_version: `v2`
- title: `Runtime concurrent start lock and generated status-surface alignment`
- research_only: `false`
- implementation_ready: `true`
- status: `needs_research`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_path: `pending://issue-materialization`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `none`
- problem: Same-project concurrent `freely start --project` invocations can pass startup conflict checks before any caller writes authoritative supervisor ownership, allowing duplicate supervisors to materialize for one worktree. Separately, `status` / `fleet-status` can keep showing stale generated worker-prompt truth from `manager-worker-launch-state.env` even after a newer continuity file exists on disk, creating a false impression that older prompts are still authoritative.
- why_now:
  - dogfood evidence on `2026-04-08 01:23:58 PDT` showed three same-second supervisors for one worker project
  - stopping that worker required hard-kill fallback, so the defect is operationally harmful rather than cosmetic
  - root `live-status` already shows the newer continuity generation, but `status` / `fleet-status` still surface old generated prompt truth and stale manager intent
- acceptance_criteria:
  - concurrent same-project `freely start --project` calls materialize at most one `supervisor_started` runtime event
  - later concurrent callers either attach/reuse or exit after bounded wait; they do not create a second supervisor
  - stale start-lock recovery is bounded and does not block future starts forever
  - `status` / `fleet-status` generated continuity/prompt surface reflects the latest valid continuity file on disk
  - `status` / `fleet-status` consumed continuity/prompt surface does not advance unless consumption truth actually advances or stale-ref repair explicitly applies
  - focused regression tests cover both the concurrent-start case and the stale-generated-surface case
- promotion_gate:
  - keep the repair inside runtime start serialization and status read-path alignment
  - do not widen into broader worker recovery policy, semantic-loop policy, or provenance research
  - preserve the existing `live-status` meaning where `generated != consumed` is allowed
- open_questions:
  - should concurrent later callers wait for the start lock to clear and then attach, or fail fast once a healthy supervisor is observed
  - should baseline/fleet explicitly annotate when generated truth was refreshed from disk rather than launch-state persistence
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author-review`
    summary: `Observed dogfood evidence proves two narrow defects: same-project duplicate supervisor bootstrap and stale generated manager intent surface. Both can be repaired without reopening broader governance families.`
    verdict: `ready_for_bounded_repair`
- next_action: Materialize the narrow repair in this worktree, add regression coverage first, then replay focused runtime status tests plus a concurrent-start regression.
- revisit_trigger: Reopen only if the lock-based repair still allows duplicate same-project supervisors, or if aligning generated prompt truth in baseline/fleet hides real consumption drift.
- decision_reason: `This is a bounded runtime correctness plus status-surface alignment repair, not a new architecture family. The observed defects are concrete, reproducible, and narrower than the surrounding restart-storm and provenance-governance families.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
