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
- blocker taxonomy: `protected_environment_only`
- not_applicable_reason: `no_distinct_real_environment_boundary`
- not_applicable_explanation: `The executable surface is the local gate and merge-governance path, not an additional hosted runtime environment.`
- replacement_evidence: `Focused gate regressions and compatibility captures are sufficient for this bounded schema owner.`

## Acceptance Items

### Freeze adequacy item v2 schema
- id: `adequacy-item-schema-v2`
- requirement: `The owner freezes richer adequacy metadata while preserving the existing five required fields.`
- evidence_level: `integration`
- status: `pending`
- artifact_ref: `pending://pretests-adequacy-schema-verification`

### Classify insufficient versus sufficient
- id: `adequacy-classification-diagnostics`
- requirement: `Gate diagnostics distinguish not-run, run-but-insufficient, and sufficient-with-evidence.`
- evidence_level: `integration`
- status: `pending`
- artifact_ref: `pending://pretests-adequacy-schema-verification`

### Preserve legacy compatibility
- id: `legacy-owner-compatibility`
- requirement: `Legacy owners remain compatible until phase policy explicitly hardens selected fields.`
- evidence_level: `integration`
- status: `pending`
- artifact_ref: `pending://pretests-adequacy-schema-verification`
