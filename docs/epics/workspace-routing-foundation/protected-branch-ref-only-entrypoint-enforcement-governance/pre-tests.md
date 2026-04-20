# Pre-Tests: protected-branch-ref-only-entrypoint-enforcement-governance

## Acceptance Targets

### AT-001 protected-branch ff-only is blocked before ref advance

- acceptance target: `git merge --ff-only` cannot advance `develop` to a feature commit without a canonical protected merge receipt
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-reference-transaction-hook`
- required evidence: `reference-transaction blocks protected-branch ff-only before HEAD moves`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 receipt-bearing protected merge commit remains valid

- acceptance target: a receipt-bearing protected merge commit can still update a protected branch under the same hook
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-reference-transaction-hook`
- required evidence: `receipt-bearing merge commit allowed on protected branch`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 merge-commit entrypoint contract remains intact

- acceptance target: the earlier guarded merge entrypoint enforcement still passes under its existing focused regressions
- testing layer: governance
- target environment: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook` plus `docs/system/workspace/scripts/tests/test-merge-guarded-hooked-initial-merge-receipt` plus `docs/system/workspace/scripts/tests/test-merge-guarded`
- required evidence: `merge-commit guarded path still valid after adding ref gate`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `Protected-branch ff-only updates fail before the protected ref moves to a non-receipted commit.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-reference-transaction-hook`

### AT-002
- id: `AT-002`
- requirement: `Receipt-bearing protected merge commits still update protected branches under the ref gate.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-reference-transaction-hook`

### AT-003
- id: `AT-003`
- requirement: `The existing merge-commit entrypoint contract remains green after the ref-only enforcement is added.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
