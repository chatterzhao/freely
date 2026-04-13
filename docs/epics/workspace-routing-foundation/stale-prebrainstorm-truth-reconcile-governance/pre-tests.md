# Pre-Tests: stale-prebrainstorm-truth-reconcile-governance

## Unit
- acceptance target: `Reconcile rules deterministically distinguish stale, superseded, deferred, and absorbed statements.`
- testing layer: `unit`
- target environment: `feature/stale-prebrainstorm-truth-reconcile-20260411`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner changes governance text and canonical pointers only; there is no separately callable unit seam below the documented reconcile rules.`
- replacement_evidence: `The reconcile matrix and the representative sample diffs are sufficient for this documentation-only owner.`

## Integration
- acceptance target: `A representative reconcile batch updates stale statements with canonical truth pointers without widening into runtime or gate logic changes.`
- testing layer: `integration`
- target environment: `feature/stale-prebrainstorm-truth-reconcile-20260411`
- required evidence: `document diff plus verification review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-pretests-gate`.
2. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `At least one superseded, one deferred, and one absorbed sample are reconciled with minimal pointer-based edits.`
- testing layer: `end_to_end`
- target environment: `documentation reconcile batch`
- required evidence: `lawful replacement evidence`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `This owner is a documentation reconcile owner; the representative batch is validated through owner docs, review receipts, and governance-check rather than a separate runtime end-to-end harness.`
- replacement_evidence: `The before/after reconcile capture is preserved in the verification artifact, and the paired develop-promote replay covers the remaining integration boundary.`

## Real-Environment
- real_environment_status: `pass`
- real_environment_reason: `This owner is documentation-only and does not require an additional real-environment test surface; the representative reconcile batch and governance-check are sufficient.`

## Acceptance Items

### Reconcile policy exists
- id: `reconcile-policy-frozen`
- requirement: `The owner freezes when a stale pre-brainstorm statement may be marked superseded, deferred, or absorbed.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/stale-prebrainstorm-truth-reconcile-governance/code-reviews/20260411-stale-prebrainstorm-truth-reconcile-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-1,tasks.md#task-2`
- case_design: `Review the owner docs and representative samples against one fixed stale/superseded/deferred/absorbed matrix before touching any historical wording.`

### Superseded sample is reconciled
- id: `representative-superseded-sample`
- requirement: `The verification-contract-and-premerge-adequacy pre-brainstorm is marked as stale/follow-on only, and no longer overclaims that a stronger adequacy gate has already landed on current develop.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/stale-prebrainstorm-truth-reconcile-governance/code-reviews/20260411-stale-prebrainstorm-truth-reconcile-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2,tasks.md#task-3`
- case_design: `Reconcile the 20260408-1205 sample against the owner issue and verification receipt, and confirm the note distinguishes owner truth from not-yet-merged feature-lane materialization.`

### Absorbed sample is reconciled
- id: `representative-absorbed-sample`
- requirement: `The nested test-pre-merge receipt audit pre-brainstorm remains clearly marked as absorbed and closed, not as an active unresolved bug.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/stale-prebrainstorm-truth-reconcile-governance/code-reviews/20260411-stale-prebrainstorm-truth-reconcile-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2,tasks.md#task-3`
- case_design: `Verify the 20260406-0055 sample still points to its absorbed owner and does not reopen an already-closed follow-on.`

### Deferred split sample is reconciled
- id: `representative-deferred-split-sample`
- requirement: `The mixed pretests-gate and network-proxy pre-brainstorm preserves deferred split scope and does not rewrite later retirement/network follow-ons as if they were already finished by the earliest owner.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/stale-prebrainstorm-truth-reconcile-governance/code-reviews/20260411-stale-prebrainstorm-truth-reconcile-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2,tasks.md#task-3`
- case_design: `Review the 20260327-0651 sample and confirm it separates earliest completion-gate truth from later retirement and proxy follow-on owners.`

### Partially materialized sample is reconciled
- id: `representative-partial-materialization-sample`
- requirement: `The feature-owned test-pre-merge family pre-brainstorm distinguishes landed promotion/lane truth from still-deferred family lifecycle automation without inventing missing owner pointers.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/stale-prebrainstorm-truth-reconcile-governance/code-reviews/20260411-stale-prebrainstorm-truth-reconcile-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-2,tasks.md#task-3`
- case_design: `Review the 20260405-1615 sample and confirm it cites only existing owner truth while leaving family lifecycle automation explicitly deferred.`

### No capability drift introduced
- id: `reconcile-no-capability-drift`
- requirement: `The reconcile batch does not introduce new runtime/gate commitments or rename pre-tests into a parallel test truth.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/stale-prebrainstorm-truth-reconcile-governance/code-reviews/20260411-stale-prebrainstorm-truth-reconcile-verification.md`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `tasks.md#task-3,tasks.md#task-4,tasks.md#task-5`
- case_design: `Run governance-check and a manual diff audit to verify the batch only adds canonical pointers and boundary notes, with no runtime/gate file changes and no tests.md parallel artifact.`

### Develop promote adequacy is bound
- id: `develop-promote-adequacy-bound`
- requirement: `The stale-prebrainstorm reconcile batch binds C-20260411-1417-B to the canonical verification-contract owner chain and remains consumable by the develop-promote replay without inventing a new execution owner.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/stale-prebrainstorm-truth-reconcile-governance/code-reviews/20260411-stale-prebrainstorm-truth-reconcile-verification.md`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `tasks.md#task-2,tasks.md#task-3,tasks.md#task-5`
- case_design: `Replay the paired pre-merge batch and confirm C-20260411-1417-B is absorbed into the canonical verification-contract owner chain, while Unit / End-to-End / Real-Environment remain lawfully marked as no_executable_boundary_at_this_layer for this documentation-only owner.`
