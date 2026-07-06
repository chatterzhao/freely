# Pre-Tests: protected-merge-unparseable-subject-receipt-gap-governance

## Unit
- acceptance target: `Parser recognizes validation_mode unparseable_subject_ancestry and rejects malformed field combinations`
- testing layer: `unit`
- target environment: `feature/protected-merge-unparseable-subject-gap-20260411`
- required evidence: `focused regression pass for malformed and valid ledger entries`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`.

## Integration
- acceptance target: `generic-subject protected-ancestry gaps pass only with matching absorbing merge truth and bounded evidence; existing parseable-subject cases do not regress`
- testing layer: `integration`
- target environment: `feature/protected-merge-unparseable-subject-gap-20260411`
- required evidence: `focused regression pass plus repository governance pass`
- blocker taxonomy: `execution_pending_or_failed`
1. Run `bash docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`.
2. Run `./bin/governance-check`.

## End-to-End
- acceptance target: `Canonical April 10 preferred-auth ancestry gaps are auditable through the new stronger-evidence path without weakening ordinary receipt-gap semantics`
- testing layer: `end_to_end`
- target environment: `develop-bound guarded merge chain`
- required evidence: `ledger entries plus governance-check pass`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `protected_environment_only`
- not_applicable_explanation: `This governance slice is consumed through repository governance and develop-bound merge flow rather than a separate operator-facing end-to-end surface.`
- replacement_evidence: `Focused regression coverage and repository-level governance-check prove the canonical contract.`

## Real-Environment
- acceptance target: `Canonical develop remains governance-green after the bounded contract lands`
- testing layer: `real_environment`
- target environment: `origin/develop`
- required evidence: `post-merge governance replay`
- blocker taxonomy: `execution_pending_or_failed`
- not_applicable_reason: `protected_environment_only`
- not_applicable_explanation: `Protected branch verification occurs only after guarded merge into develop.`
- replacement_evidence: `Feature-lane governance-check plus focused regressions prove pre-merge readiness.`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `A generic-subject protected-ancestry merge without an explicit unparseable-subject contract entry fails governance-check.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`

### AT-002
- id: `AT-002`
- requirement: `A generic-subject ancestry merge passes only when the explicit stronger-evidence schema matches the absorbing protected merge and bounded owner evidence.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`

### AT-003
- id: `AT-003`
- requirement: `Wrong absorbing protected merge truth is rejected for unparseable-subject ancestry entries.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`

### AT-004
- id: `AT-004`
- requirement: `Under-evidenced generic-subject entries fail closed when bounded owner or verification fields are missing.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`

### AT-005
- id: `AT-005`
- requirement: `Existing parseable-subject receipt-gap cases remain green after the new validation mode lands.`
- evidence_level: `integration`
- status: `pass`
- red-green-status: not_applicable
- red-green-not-applicable-reason: historical issue completed before TDD RED-GREEN requirement
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
