# Pre-Tests: protected-branch-ref-only-entrypoint-enforcement-governance

## Unit
- acceptance target: `Do not invent a fake unit boundary for a hook-routing repair whose meaningful behavior only exists at the Git protected-ref integration surface.`
- testing layer: `unit`
- target environment: `feature/protected-branch-ff-only-gate-20260419`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner adds a Git hook wrapper and ref-transaction policy check; the smallest truthful executable surface is the guarded Git integration flow, not an isolated unit seam.`
- replacement_evidence: `The focused hook regressions and guarded merge regressions below are the first executable boundary that can prove protected-ref behavior.`

## Integration
- acceptance target: `Prove protected-branch ref-only advances are blocked locally while canonical receipt-bearing merge commits still pass.`
- testing layer: `integration`
- target environment: `feature/protected-branch-ff-only-gate-20260419`
- required evidence: `focused regression output plus governance verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-reference-transaction-hook`.
2. Run `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`.
3. Run `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded-hooked-initial-merge-receipt`.
4. Run `bash docs/system/workspace/scripts/tests/test-pr-merge-guarded`.
5. Run `git diff --check`.
6. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `Keep the lawful feature -> test-pre-merge -> develop guarded chain intact after adding ref-only protected-branch enforcement.`
- testing layer: `end_to_end`
- target environment: `guarded protected-branch merge chain`
- required evidence: `guarded merge receipts plus verification artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Merge `feature/protected-branch-ff-only-gate-20260419` into a disposable `test-pre-merge-*` branch via `freely pr-merge-guarded`.
2. Merge that `test-pre-merge-*` branch into `develop` via `freely pr-merge-guarded`.
3. Confirm the protected-root merge path accepts the receipt-bearing merge commit while rejecting non-receipted ref-only updates.

## Real-Environment
- acceptance target: `Publish the protected-branch repair to canonical develop and retire the temporary merge lanes instead of leaving local-only proof behind.`
- testing layer: `real_environment`
- target environment: `local protected root plus origin/develop`
- required evidence: `push result and temporary branch/worktree retirement evidence`
- blocker taxonomy: `execution_pending_or_failed`
1. Push `develop` to `origin/develop`.
2. Delete branch `test-pre-merge-20260419-protected-ref-only-entrypoint`.
3. Remove `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260419-feature-protected-branch-ff-only-gate`.
4. Delete branch `feature/protected-branch-ff-only-gate-20260419`.
- real_environment_status: `pass`
- real_environment_reason: `This owner changes local Git governance, not an external hosted runtime. The meaningful real-environment surface is canonical develop publication plus retirement of the temporary merge lanes.`

## Acceptance Items

### Protected ref-only advance is blocked before HEAD moves
- id: `protected-ref-ff-only-block`
- requirement: `Protected branches fail closed when a ref-only update tries to advance them to a non-receipted commit.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/protected-branch-ref-only-entrypoint-enforcement-governance/code-reviews/20260419-protected-branch-ref-only-entrypoint-enforcement-verification.md`

### Receipt-bearing protected merge commit still succeeds
- id: `protected-ref-receipt-allow`
- requirement: `The new ref gate preserves canonical protected merge commits that already carry a valid guarded merge receipt.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/protected-branch-ref-only-entrypoint-enforcement-governance/code-reviews/20260419-protected-branch-ref-only-entrypoint-enforcement-verification.md`

### Guarded premerge promote remains lawful under the new ref gate
- id: `protected-ref-guarded-promote`
- requirement: `Feature -> test-pre-merge -> develop guarded replay remains valid after adding protected ref-only enforcement.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#2,tasks.md#3,tasks.md#4`
- case_design: `Run the focused reference-transaction and guarded merge regressions in the feature lane, then replay the feature through a disposable test-pre-merge branch into develop via pr-merge-guarded and require the protected branch to accept only the receipt-bearing merge commit.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/protected-branch-ref-only-entrypoint-enforcement-governance/code-reviews/20260419-protected-branch-ref-only-entrypoint-enforcement-verification.md`
