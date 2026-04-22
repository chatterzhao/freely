# Candidates - 20260421-1200--runtime-daemon-self-loop-followthrough

## Context
- Source brainstorm: `docs/pre-brainstorms/20260421-1200--runtime-daemon-self-loop-followthrough/brainstorms.md`
- Status: `promoted`
- Route: `materialize-daemon-self-loop-followthrough-owner-and-replay-through-guarded-develop`

## Candidates

### C-20260421-1200-A
- candidate_format_version: `v2`
- title: `Runtime daemon self-loop followthrough governance`
- research_only: `false`
- implementation_ready: `true`
- status: `promoted`
- milestone: `M-20260306-workspace-routing-foundation`
- priority: `P0`
- promoted_issue_id: `I-20260421-1200-A`
- promoted_issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
  - `docs/epics/workspace-routing-foundation/three-loop-lifecycle-single-source-governance-followthrough/issues/three-loop-lifecycle-single-source-governance-followthrough.md`
- problem: Dogfooding proved a remaining runtime-control blocker: daemon-mode Freely could stop self-looping after a patrol round because an unexpected `TERM` was recorded as `operator_stop`, and a lone dispatcher/watchdog residue could also falsely block the next `start` or `daemon start`.
- followthrough_update: Guarded replay then exposed two same-owner seams on canonical `develop`: runtime could not consume the current `## Worker Delegation` continuity shape into worker launches, and after that repair it could still auto-recover a `merged-clean` blocker worktree instead of routing it to cleanup followthrough retirement.
- followthrough_update_2: The same autonomous-loop owner then exposed one more control-plane seam: manager and worker AI rounds could exit without a machine-checkable closeout contract, so runtime had no reliable way to distinguish `stop_ai`, `resume_manager`, `delegate_workers`, `worker_done`, `worker_blocked`, and `worker_handoff_needed`, nor to force a precise same-session repair when the artifact was missing.
- followthrough_update_3: Canonical `develop` replay then exposed a narrower cleanup-handoff retirement seam: manager could select a real cleanup-governance task and materialize a lawful worker prompt, but the worker worktree was still auto-settled as `retire_ready_merged_worker` before it could execute the external cleanup surfaces named in that prompt.
- why_now:
  - this blocker prevents Freely from autonomously selecting, finishing, and closing tasks on canonical `develop`
  - the fix is already implemented and focused regressions are green in the blocker worktree, but guarded develop promotion still needs lawful owner evidence
  - the newest repair must preserve cleanup-handoff workers that carry full verification metadata plus external cleanup scope, otherwise canonical `develop` still cannot finish even its first real selected task
  - the final acceptance surface is not "daemon stayed up once" but "Freely continued self-work end-to-end and then moved to the next task"
- acceptance_criteria:
  - `start` and `daemon start` no longer reject because of orphaned watchdog/dispatcher residue when no authoritative supervisor exists
  - daemon supervisor ignores unexpected `TERM` without `stop.marker` and still honors explicit daemon stop
  - runtime consumes current `## Worker Delegation` continuity into worker launches instead of stalling after manager selection
  - `merged-clean` / `retire-ready` blocker worktrees are settled toward cleanup followthrough retirement rather than being auto-recovered as edit workers
  - cleanup-handoff workers that still need to reconcile external owner surfaces are not reclaimed or auto-settled merely because their branch is already merged into `develop`
  - every manager / worker AI cycle now leaves exactly one valid exit contract artifact, or runtime reuses the precise resume target to repair that artifact before doing broader work
  - guarded `feature/* -> test-pre-merge-* -> develop` replay succeeds with concrete owner evidence
  - on canonical `develop`, `freely daemon start` autonomously selects at least one task, completes it to the current-project success standard, closes the temporary worktree, and continues to another task
- promotion_gate:
  - keep scope on the runtime self-loop blocker and its bounded governance followthrough only
  - do not widen into general scan/task-picking redesign in this owner
  - require final develop-side self-host acceptance before declaring completion
- open_questions:
  - whether future start-mode UI affordances should expose scan item ids directly now that runtime selection can be parameterized
  - whether unexpected daemon signals need a broader observability taxonomy later
- acceptance_reviews:
  - reviewer: `codex`
    mode: `author review`
    summary: `The field blocker is runtime-control-plane specific. The smallest truthful owner is a followthrough lane that repairs orphan precheck truth, ignores unexpected daemon TERM without stop intent, and proves canonical develop self-host continuity.`
    verdict: `ready_for_issue_materialization`
- next_action: Candidate mirror only. `I-20260421-1200-A` remains the canonical owner for the daemon self-loop followthrough, the guarded-replay-discovered continuity/retirement seams, final self-host acceptance on `develop`, and retirement of the temporary blocker worktree and test-pre-merge branch.
- revisit_trigger: Re-open only if canonical `develop` still falls out of autonomous looping after this bounded repair, or if another blocker shows the self-loop boundary needs a larger dedicated runtime owner.
- decision_reason: `This is a concrete post-architecture runtime blocker with already-bounded code changes. A narrow followthrough owner is safer and more truthful than reopening the broader runtime architecture lanes.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
