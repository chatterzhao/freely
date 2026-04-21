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
- why_now:
  - this blocker prevents Freely from autonomously selecting, finishing, and closing tasks on canonical `develop`
  - the fix is already implemented and focused regressions are green in the blocker worktree, but guarded develop promotion still needs lawful owner evidence
  - the final acceptance surface is not "daemon stayed up once" but "Freely continued self-work end-to-end and then moved to the next task"
- acceptance_criteria:
  - `start` and `daemon start` no longer reject because of orphaned watchdog/dispatcher residue when no authoritative supervisor exists
  - daemon supervisor ignores unexpected `TERM` without `stop.marker` and still honors explicit daemon stop
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
- next_action: Candidate mirror only. `I-20260421-1200-A` is now the canonical owner for the daemon self-loop followthrough, guarded develop replay, final self-host acceptance, and retirement of the temporary blocker worktree and test-pre-merge branch.
- revisit_trigger: Re-open only if canonical `develop` still falls out of autonomous looping after this bounded repair, or if another blocker shows the self-loop boundary needs a larger dedicated runtime owner.
- decision_reason: `This is a concrete post-architecture runtime blocker with already-bounded code changes. A narrow followthrough owner is safer and more truthful than reopening the broader runtime architecture lanes.`
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
