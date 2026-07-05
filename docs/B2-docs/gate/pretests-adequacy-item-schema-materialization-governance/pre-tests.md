# Pre-Tests: pretests-adequacy-item-schema-materialization-governance

## Unit
- acceptance target: `Schema parsing and adequacy classification remain deterministic for both legacy and v2 items.`
- testing layer: `unit`
- target environment: `feature/pretests-adequacy-item-schema-materialization-20260411`
- required evidence: `focused gate regression output`
- blocker taxonomy: `definition_missing`
1. Run `bash docs/system/workspace/scripts/tests/test-pretests-gate`.

## Integration
- acceptance target: `Gate diagnostics distinguish not-run, run-but-insufficient, and sufficient-with-evidence without breaking legacy owners.`
- testing layer: `integration`
- target environment: `feature/pretests-adequacy-item-schema-materialization-20260411`
- required evidence: `command output plus verification review artifact`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-pretests-gate`.
2. Run `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`.
3. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `A new owner can adopt v2 adequacy metadata and be selectively enforced without regressing legacy owner paths.`
- testing layer: `end_to_end`
- target environment: `feature/pretests-adequacy-item-schema-materialization-20260411`
- required evidence: `one new-owner path plus one legacy-owner compatibility path`
- blocker taxonomy: `execution_pending_or_failed`
1. Capture one v2-enforced owner path and one legacy-compatible path in the verification artifact.

## Real-Environment
- acceptance target: `This owner is bounded to governance and gate semantics; no separate hosted real-environment surface is introduced.`
- testing layer: `real_environment`
- target environment: `local gate boundary`
- required evidence: `lawful replacement evidence recorded in verification artifact`
- blocker taxonomy: `definition_missing`
- not_applicable_reason: `no_executable_boundary_at_this_layer`
- not_applicable_explanation: `The executable surface is the local gate and merge-governance path, not an additional hosted runtime environment.`
- replacement_evidence: `Focused gate regressions and compatibility captures are sufficient for this bounded schema owner.`

## Acceptance Items

### Freeze adequacy item v2 schema
- id: `adequacy-item-schema-v2`
- requirement: `The owner freezes richer adequacy metadata while preserving the existing five required fields.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Freeze adequacy item schema v2 and keep the new fields optional for untouched legacy owners.`
- case_design: `Use the feature-lane verification review to prove the same Acceptance Item now carries adequacy-v2 metadata without regressing legacy parsing.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/pretests-adequacy-item-schema-materialization-governance/code-reviews/20260411-pretests-adequacy-item-schema-materialization-verification.md`

### Classify insufficient versus sufficient
- id: `adequacy-classification-diagnostics`
- requirement: `Gate diagnostics distinguish not-run, run-but-insufficient, and sufficient-with-evidence.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Add focused regressions that differentiate missing adequacy-v2 coverage, insufficient evidence level, and stale artifact reuse.`
- case_design: `Replay standalone and guarded gate fixtures that each fail for a different adequacy reason, then confirm the final feature-lane verification artifact records the distinct verdicts.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/pretests-adequacy-item-schema-materialization-governance/code-reviews/20260411-pretests-adequacy-item-schema-materialization-verification.md`

### Preserve legacy compatibility
- id: `legacy-owner-compatibility`
- requirement: `Legacy owners remain compatible until phase policy explicitly hardens selected fields.`
- surface_kind: `integration`
- target_lane: `feature-local`
- promotion_gate: `completion`
- task_refs: `Keep legacy owners on the compatibility path while hardening new-owner and develop-bound adequacy checks.`
- case_design: `Retain an unchanged legacy fixture in gate tests while a new-owner fixture opts into adequacy-v2 and guarded develop promote enforcement.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/pretests-adequacy-item-schema-materialization-governance/code-reviews/20260411-pretests-adequacy-item-schema-materialization-verification.md`

### Guarded develop promote proves adequacy-v2 coverage
- id: `develop-promote-adequacy-proof`
- requirement: `A guarded test-pre-merge promote proves the owner now carries explicit adequacy-v2 coverage for develop-bound merge, rather than relying on feature-local completion evidence alone.`
- surface_kind: `integration`
- target_lane: `premerge-integration`
- promotion_gate: `develop_merge`
- task_refs: `Replay guarded premerge promotion on a test-pre-merge batch and confirm the owner now carries a distinct develop-merge adequacy statement with fresh staged review evidence.`
- case_design: `Merge the feature lane into a disposable test-pre-merge batch through pr-merge-guarded, run premerge-integration gate regressions there, and use the resulting verification artifact to prove the lane/gate pair is now explicitly covered.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/epics/workspace-routing-foundation/pretests-adequacy-item-schema-materialization-governance/code-reviews/20260411-pretests-adequacy-item-schema-materialization-verification.md`
