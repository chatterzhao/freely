# Pre-Tests: three-loop-lifecycle-single-source-governance-followthrough

## Unit
- acceptance target: `Do not invent a fake executable unit seam for a governance-only documentation followthrough that changes no runtime behavior.`
- testing layer: `unit`
- target environment: `feature/three-loop-model-refactor-20260418`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `pass`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner only closes lifecycle-governance documentation around a canonical truth source and downstream consumer sync expectations. It does not introduce a separately callable unit.`
- replacement_evidence: `The smallest executable boundary is lifecycle validation through pretests-gate, governance-check, and the bounded verification artifact captured below.`

## Integration
- acceptance target: `Prove the single-source governance followthrough owner has a complete issue-bound verification contract before guarded replay.`
- testing layer: `integration`
- target environment: `feature/three-loop-model-refactor-20260418`
- required evidence: `command output plus verification artifact`
- blocker taxonomy: `pass`
1. Run `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260418-feature-three-loop-model-refactor --issue docs/B2-docs/ibm/three-loop-lifecycle-single-source-governance-followthrough/issues/three-loop-lifecycle-single-source-governance-followthrough.md`.
2. Run `git diff --check`.
3. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `Keep the guarded feature -> test-pre-merge -> develop chain lawful while carrying concrete owner evidence for the three-loop single-source governance closeout.`
- testing layer: `end_to_end`
- target environment: `guarded develop-bound merge chain`
- required evidence: `merge receipts plus verification artifact`
- blocker taxonomy: `pass`
1. Merge `feature/three-loop-model-refactor-20260418` into `test-pre-merge-three-loop-governance-20260419` via `freely pr-merge-guarded`.
2. Run `./bin/governance-check` in `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260419-test-pre-merge-three-loop-governance`.
3. Merge `test-pre-merge-three-loop-governance-20260419` into `develop` via `freely pr-merge-guarded`.

## Real-Environment
- acceptance target: `Record canonical develop publication and retirement of the temporary feature and test-pre-merge worktrees as the final protected-branch acceptance surface.`
- testing layer: `real_environment`
- target environment: `local fleet plus origin/develop`
- required evidence: `protected branch push result and temporary worktree retirement evidence`
- blocker taxonomy: `pass`
1. Push `develop` to `origin/develop`.
2. Remove `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260419-test-pre-merge-three-loop-governance`.
3. Delete branch `test-pre-merge-three-loop-governance-20260419`.
4. Remove `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260418-feature-three-loop-model-refactor`.
5. Delete branch `feature/three-loop-model-refactor-20260418`.
6. Re-run `git worktree list` and confirm both temporary worktrees are gone.
- real_environment_status: `pass`
- real_environment_reason: `This owner is governance-only. The meaningful protected-branch surface is canonical develop absorption plus retirement of the temporary worktrees, not a separate hosted runtime environment.`

## Acceptance Items

### Single-source owner chain exists for the develop-bound docs diff
- id: `three-loop-single-source-owner-chain`
- requirement: `The governance-only docs diff is paired with a concrete candidate, issue, pre-tests, tasks, progress, and verification artifact so protected merge no longer sees a completed-family reopen without lawful owner evidence.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/three-loop-lifecycle-single-source-governance-followthrough/code-reviews/20260428-three-loop-state-closeout-verification.md`

### Canonical lifecycle document remains the only detailed truth
- id: `three-loop-single-detailed-truth`
- requirement: `The touched active truth set keeps docs/system/workspace/three-loop-capability-lifecycle.md as the only detailed whole-app lifecycle specification.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#2`
- case_design: `Read the touched active truth files together and confirm the detailed lifecycle model lives only in the canonical document, while the other files defer to it rather than restating the same depth locally.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/three-loop-lifecycle-single-source-governance-followthrough/code-reviews/20260428-three-loop-state-closeout-verification.md`

### Consumer docs require read-and-sync behavior
- id: `three-loop-consumer-read-sync-contract`
- requirement: `Touched agent and skill docs tell future authors to read and sync against the canonical lifecycle truth when lifecycle semantics matter, instead of co-maintaining another detailed specification.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#2`
- case_design: `Inspect the touched agent and skill docs and confirm they use the canonical lifecycle document as the detailed source of truth while preserving only the local consumer contract they need.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/three-loop-lifecycle-single-source-governance-followthrough/code-reviews/20260428-three-loop-state-closeout-verification.md`

### Guarded merge path preserves the governance closeout
- id: `three-loop-single-source-guarded-merge`
- requirement: `Feature -> test-pre-merge -> develop guarded replay preserves the single-source governance closeout and retires the temporary worktrees after publication.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#3,tasks.md#4`
- case_design: `Merge the current feature into the disposable three-loop test-pre-merge batch, keep governance-check green there, then guardedly replay that batch into develop so the develop gate consumes this new owner chain instead of rejecting the completed-family followthrough.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/ibm/three-loop-lifecycle-single-source-governance-followthrough/code-reviews/20260428-three-loop-state-closeout-verification.md`

## Acceptance (state-closeout addendum 2026-04-28)

- acceptance target: `Governance-only state reconciliation closeout: confirm that the three-loop lifecycle single-source truth is already in develop and only state tracking needs updating.`
- testing layer: `premerge-integration`
- target environment: `feature/three-loop-state-closeout-20260428 → test-pre-merge-three-loop-closeout-20260428 → develop`
- required evidence: `fresh staged owner review artifact`
- blocker taxonomy: `pass`
- artifact_ref: `docs/B2-docs/ibm/three-loop-lifecycle-single-source-governance-followthrough/code-reviews/20260428-three-loop-state-closeout-verification.md`

- artifact_ref: `docs/B2-docs/ibm/three-loop-lifecycle-single-source-governance-followthrough/code-reviews/20260428-three-loop-state-closeout-verification.md`
