# Pre-Tests: runtime-startup-self-healing-governance

## Unit
- acceptance target: `Do not invent a fake lower-level seam; the smallest executable boundaries here are focused runtime script regressions.`
- testing layer: `unit`
- target environment: `feature/runtime-startup-self-healing-boundary-20260419`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner changes runtime shell orchestration and status readback, so the lawful executable seams are the focused shell regressions and guarded replay below.`
- replacement_evidence: `Focused startup-self-heal and launch-state persistence regressions capture the smallest executable behavior changes.`

## Integration
- acceptance target: `Prove startup self-heal clears stale machine-owned truth without breaking adjacent status/continuity surfaces.`
- testing layer: `integration`
- target environment: `feature/runtime-startup-self-healing-boundary-20260419`
- required evidence: `focused regression output plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash -n docs/system/workspace/scripts/runtime/freely`.
2. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status-startup-self-heals-stale-runtime-state`.
3. Run `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-persists-stale-continuity-rewrite`.
4. Run `bash docs/system/workspace/scripts/tests/test-freely-stale-manager-continuity-filter`.
5. Run `bash docs/system/workspace/scripts/tests/test-freely-live-status`.
6. Run `./bin/governance-check`.
7. Run `git diff --check`.

## End-to-End
- acceptance target: `Promote the bounded startup self-heal owner through canonical develop instead of treating feature-lane replay as final absorption.`
- testing layer: `end_to_end`
- target environment: `guarded develop-bound merge chain`
- required evidence: `merge receipts plus verification artifacts`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/runtime-startup-self-healing-boundary-20260419` into canonical `develop`.
2. Push `develop` after final verification evidence is written back.
3. Delete the dedicated feature worktree and branch after develop carries the absorbed owner.

## Real-Environment
- acceptance target: `Use protected-root replay to prove stale startup truth self-heals under the real runtime entrypoint, not only in synthetic tests.`
- testing layer: `real_environment`
- target environment: `canonical protected root`
- required evidence: `protected-root live replay plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Inspect the protected root stale state before replay.
2. Run `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely` and confirm startup self-heal canonicalizes stale machine state.
3. Run `./bin/freely daemon start --project /Users/zhaoyu/Downloads/code/my-freely/freely`, wait through the startup grace window, and verify the runtime no longer remains in contradictory fake-up state.

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `startup status reads clear stale runtime pid files and downgrade stale startup truth when no authoritative runtime processes exist.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/code-reviews/20260419-runtime-startup-self-healing-verification.md`

### AT-002
- id: `AT-002`
- requirement: `launch-state continuity/prompt references are persisted after status refresh rewrites stale continuity anchors.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/code-reviews/20260419-runtime-startup-self-healing-verification.md`

### AT-003
- id: `AT-003`
- requirement: `protected-root replay proves the runtime no longer stays stuck in fake running/up startup truth after stale-machine-state cold start.`
- evidence_level: `real_environment`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/code-reviews/20260419-runtime-startup-self-healing-verification.md`
