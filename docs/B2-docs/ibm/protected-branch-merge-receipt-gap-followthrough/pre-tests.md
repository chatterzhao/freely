# Pre-Tests: protected-branch-merge-receipt-gap-followthrough

## Acceptance Targets

### AT-001 missing ancestry gap fails closed

- acceptance target: `governance-check` rejects trailerless protected-ancestry merges after the audit effective date when no matching ordinary backfill entry exists
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- required evidence: `no-backfill failure case`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 matching ordinary backfill passes

- acceptance target: ordinary trailerless merge commits pass audit once the canonical backfill ledger matches the merge subject/source pair
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- required evidence: `develop-target and feature-target pass cases`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 trailer-bearing merges cannot claim backfill

- acceptance target: protected merges that already carry canonical receipts are rejected if they also appear in the ordinary receipt-gap ledger
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- required evidence: `trailer-bearing rejection case`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 break-glass receipts remain separate

- acceptance target: ordinary receipt-gap auditing does not absorb break-glass receipt policy, and canonical governance still validates both surfaces together
- testing layer: governance
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt` plus `./bin/governance-check`
- required evidence: `break-glass path still passes while ordinary gap audits stay green`
- blocker taxonomy: `execution_pending_or_failed`

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `A trailerless protected-ancestry merge without a matching backfill entry fails governance-check.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`

### AT-002
- id: `AT-002`
- requirement: `Matching ordinary backfill entries pass for both direct develop merges and develop -> feature ancestry merges that later enter protected ancestry.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`

### AT-003
- id: `AT-003`
- requirement: `Trailer-bearing protected merges cannot use the ordinary receipt-gap ledger as a redundant backfill path.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`

### AT-004
- id: `AT-004`
- requirement: `Break-glass receipt auditing remains independent while repository-level governance still passes.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt`
