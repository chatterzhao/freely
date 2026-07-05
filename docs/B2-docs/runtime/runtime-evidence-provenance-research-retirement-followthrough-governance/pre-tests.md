# Pre-Tests: runtime-evidence-provenance-research-retirement-followthrough-governance

## Unit
- acceptance target: `Do not invent a fake unit boundary for a docs-and-cleanup followthrough that changes no runtime behavior.`
- testing layer: `unit`
- target environment: `feature/runtime-evidence-provenance-research-retirement-20260409`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner only materializes lifecycle artifacts and retirement intent; it does not introduce a separately callable executable unit.`
- replacement_evidence: `The smallest executable boundary is lifecycle validation through pretests-gate and governance-check, both captured below at integration level.`

## Integration
- acceptance target: `Prove the followthrough owner has a complete issue-bound verification contract before guarded replay.`
- testing layer: `integration`
- target environment: `feature/runtime-evidence-provenance-research-retirement-20260409`
- required evidence: `command output plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `./bin/pretests-gate --project "$PWD" --issue docs/B2-docs/runtime/runtime-evidence-provenance-research-retirement-followthrough-governance/issues/runtime-evidence-provenance-research-retirement-followthrough-governance.md`.
2. Run `git diff --check`.
3. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `Keep the guarded feature -> test-pre-merge -> develop chain lawful while carrying retirement followthrough evidence for the dropped research packet.`
- testing layer: `end_to_end`
- target environment: `guarded develop-bound merge chain`
- required evidence: `merge receipts plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/runtime-evidence-provenance-research-retirement-20260409` into `test-pre-merge-runtime-evidence-provenance-retirement-20260409` via `freely pr-merge-guarded`.
2. Merge `test-pre-merge-runtime-evidence-provenance-retirement-20260409` into `develop` via `freely pr-merge-guarded`.
3. Confirm the guarded push path now sees a concrete owner chain instead of only candidate-level retirement notes.

## Real-Environment
- acceptance target: `Record real fleet retirement and protected-branch publication as a separate surface instead of pretending premerge alone closed the worktree lifecycle.`
- testing layer: `real_environment`
- target environment: `local fleet plus origin/develop`
- required evidence: `protected branch push result and obsolete worktree retirement evidence`
- blocker taxonomy: `execution_pending_or_failed`
1. Push `develop` to `origin/develop`.
2. Remove `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260407-060440-feature-runtime-evidence-provenance-and-canonical-absorption-gate`.
3. Delete branch `feature/runtime-evidence-provenance-and-canonical-absorption-gate-20260407-060440`.
4. Re-run `git worktree list --porcelain` and confirm the obsolete research worktree is gone.

## Acceptance Items

### Followthrough owner exists for the develop-bound retirement diff
- id: `retirement-followthrough-owner-chain`
- requirement: `The dropped research candidate is paired with a concrete issue, pre-tests, progress, and verification artifact so protected push no longer sees candidate-only evidence.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-evidence-provenance-research-retirement-followthrough-governance/code-reviews/20260409-runtime-evidence-provenance-research-retirement-followthrough-verification.md`

### Guarded merge path preserves the retirement closure
- id: `retirement-followthrough-guarded-merge`
- requirement: `Feature -> test-pre-merge -> develop guarded replay preserves the retirement followthrough without reopening the mixed-owner packet.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-evidence-provenance-research-retirement-followthrough-governance/code-reviews/20260409-runtime-evidence-provenance-research-retirement-followthrough-verification.md`

### Obsolete research worktree is retired after publication
- id: `retirement-followthrough-fleet-closeout`
- requirement: `Once canonical develop absorbs the closeout owner, the obsolete research worktree and branch are removed from the active fleet.`
- evidence_level: `real_env`
- status: `pass`
- artifact_ref: `docs/B2-docs/runtime/runtime-evidence-provenance-research-retirement-followthrough-governance/code-reviews/20260409-runtime-evidence-provenance-research-retirement-followthrough-verification.md`
