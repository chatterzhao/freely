# Pre-Tests: structured-closeout-gate-context-and-review-evidence-governance

## Unit
- acceptance target: `Structured closeout field parsing is deterministic and missing lane/gate/evidence-policy data is surfaced as data, not guessed from free-text shell fragments.`
- testing layer: `unit`
- target environment: `feature/structured-closeout-gate-and-review-evidence-followon-20260412`
- required evidence: `focused runtime/state regression output or lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner primarily changes shell-runtime contract flow, and the smallest useful executable boundary is covered by focused runtime regressions rather than a separate unit harness.`
- replacement_evidence: `Focused runtime and cleanup regressions are sufficient for the smallest executable boundary in this package.`

## Integration
- acceptance target: `Delegated intake, worker runtime state, cleanup replay, and guarded merge diagnostics consume one structured closeout contract.`
- testing layer: `integration`
- target environment: `feature/structured-closeout-gate-and-review-evidence-followon-20260412`
- required evidence: `command output plus owner review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run focused runtime verification-contract regressions.
2. Run focused cleanup replay regressions.
3. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `A guarded feature -> test-pre-merge -> develop chain blocks with explicit lane/gate/review-evidence diagnostics before final promote confusion can recur.`
- testing layer: `end_to_end`
- target environment: `test-pre-merge closeout replay and guarded develop promote`
- required evidence: `guarded replay trace plus owner review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Replay one guarded `test-pre-merge-* -> develop` chain where adequacy exists but fresh staged owner review evidence is missing, then prove the new contract surfaces that exact blocker earlier.

## Real-Environment
- acceptance target: `This owner hardens local governance/runtime contract recovery; no separate hosted environment is introduced before canonical develop promote.`
- testing layer: `real_environment`
- target environment: `local governance/runtime boundary`
- required evidence: `lawful replacement evidence recorded in owner review artifact`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The bounded surface is local runtime/governance contract recovery rather than a hosted external system.`
- replacement_evidence: `Focused runtime regressions and one guarded replay trace are sufficient for this owner's first bounded slice.`

## Acceptance Items

### Structured closeout context is persisted
- id: `structured-closeout-context-persisted`
- requirement: `Delegated intake and worker runtime state persist closeout lane, promotion gate, adequacy requirement, and review-artifact policy as first-class verification fields.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/code-reviews/20260412-structured-closeout-gate-context-and-review-evidence-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1,tasks.md#task-2`
- case_design: `Launch a worker with full structured closeout metadata, then inspect delegated intake and workcell state for the same explicit field set instead of a lone free-text closeout command.`

### Cleanup replay consumes structured fields
- id: `cleanup-replay-consumes-structured-closeout`
- requirement: `Cleanup and retirement replay read structured closeout fields directly and fail closed when those fields are incomplete.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/code-reviews/20260412-structured-closeout-gate-context-and-review-evidence-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2,tasks.md#task-3`
- case_design: `Replay cleanup with a worker snapshot that lacks structured lane/gate fields and prove the system retains the worktree with explicit missing-field diagnostics instead of best-effort parsing.`

### Guarded develop promote explains fresh review evidence requirement
- id: `develop-promote-fresh-review-evidence-diagnostic`
- requirement: `Guarded develop promote explicitly states when the remaining blocker is missing fresh staged owner review evidence, even when owner pre-tests already carry the correct lane/gate adequacy item.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/code-reviews/20260412-structured-closeout-gate-context-and-review-evidence-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-3,tasks.md#task-4,tasks.md#task-5`
- case_design: `Run one guarded premerge replay where the owner has a valid premerge adequacy item but no fresh staged owner review artifact, then confirm diagnostics name that exact missing evidence policy before final develop merge confusion.`

### No gate relaxation
- id: `no-gate-relaxation`
- requirement: `This owner does not loosen existing pretests-gate or governance-merge-gate protections while improving contract observability and replay guidance.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/structured-closeout-gate-context-and-review-evidence-governance/code-reviews/20260412-structured-closeout-gate-context-and-review-evidence-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-4,tasks.md#task-5`
- case_design: `Replay the current guarded merge failure mode and confirm it still blocks, but now points to structured closeout fields and fresh staged owner review evidence rather than only a late opaque gate miss.`
