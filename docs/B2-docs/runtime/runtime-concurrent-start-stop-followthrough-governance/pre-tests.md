# Pre-Tests: runtime-concurrent-start-stop-followthrough-governance

## Unit
- acceptance target: `Do not invent a fake unit seam for a bounded runtime followthrough whose executable proof lives in focused runtime script regressions.`
- testing layer: `unit`
- target environment: `runtime concurrent start-stop followthrough package`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner changes the integrated runtime script behavior around bootstrap attach, stop, and stop-marker preservation. The smallest stable executable seams are the focused script regressions tracked at integration level.`
- replacement_evidence: `Focused runtime script regressions plus governance-check prove the bounded contract without inventing a narrower callable unit.`

## Integration
- acceptance target: `Prove the bounded same-project bootstrap/stop followthrough holds without regressing adjacent command semantics or already-landed generated-truth surfaces.`
- testing layer: `integration`
- target environment: `runtime/freely and adjacent status surfaces`
- required evidence: `focused regression output plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-freely-start-cleans-stale-project-start-lock`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-does-not-double-launch-during-degraded-starting-grace`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`.
5. Run `bash docs/system/workspace/scripts/tests/test-freely-status-latest-generated-manager-continuity-surface`.
6. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface`.
7. Run `bash docs/system/workspace/scripts/tests/test-freely-restart-storm-status-surface`.
8. Run `git diff --check`.
9. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `Preserve a lawful feature -> test-pre-merge -> develop promotion chain for the remaining runtime followthrough instead of merging candidate-only closeout notes.`
- testing layer: `end_to_end`
- target environment: `guarded develop-bound merge chain`
- required evidence: `merge receipts plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/runtime-concurrent-start-stop-followthrough-20260411` into its guarded `test-pre-merge-*` lane via `freely pr-merge-guarded`.
2. Merge that `test-pre-merge-*` lane into `develop` via `freely pr-merge-guarded`.
3. Confirm the generated-truth status half remains out of scope while the runtime followthrough lands canonically.

## Real-Environment
- acceptance target: `Reserve canonical closeout replay and develop publication as a later tracked-root step instead of pretending feature-lane regressions alone close the lifecycle.`
- testing layer: `real_environment`
- target environment: `canonical develop in the tracked root`
- required evidence: `tracked-root replay plus canonical closeout verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `protected_environment_only`
- not_applicable_explanation: `Protected publication and any later develop push happen only after canonical develop absorbs this bounded owner.`
- replacement_evidence: `Tracked-root replay of the focused regressions plus governance-check will close the owner after guarded merge.`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Degraded bootstrap attach remains single-supervisor and reuse-friendly.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-ensure-manager-does-not-double-launch-during-degraded-starting-grace`

### AT-002
- id: `AT-002`
- requirement: `Stale project-scoped start locks do not block future lawful startup.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-start-cleans-stale-project-start-lock`

### AT-003
- id: `AT-003`
- requirement: `Project stop terminates all same-project supervisors and preserves stop intent until the last one exits.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`

### AT-004
- id: `AT-004`
- requirement: `Adjacent project command semantics stay green.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-freely-project-command-semantics`

### AT-005
- id: `AT-005`
- requirement: `Already-landed generated-truth status surfaces remain green.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-concurrent-start-stop-followthrough-governance/code-reviews/20260411-runtime-concurrent-start-stop-followthrough-verification.md`
