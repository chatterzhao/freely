# Pre-Tests: protected-merge-unparseable-subject-receipt-gap-governance

## Acceptance Targets

### AT-001 generic-subject ancestry gap fails without new contract

- acceptance target: `governance-check` rejects trailerless protected-ancestry merges with generic subjects when no explicit unparseable-subject contract entry exists
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- required evidence: `generic-subject no-backfill failure case`
- blocker taxonomy: `execution_pending_or_failed`

### AT-002 valid unparseable-subject entry passes

- acceptance target: a generic-subject ancestry merge passes only when the new explicit stronger-evidence schema matches the absorbing protected merge and bounded owner evidence
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- required evidence: `one valid generic-subject passing case`
- blocker taxonomy: `execution_pending_or_failed`

### AT-003 wrong absorbing merge fails closed

- acceptance target: `governance-check` rejects unparseable-subject entries that point at an absorbing merge not carrying the matching protected batch truth
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- required evidence: `wrong absorbing merge rejection case`
- blocker taxonomy: `execution_pending_or_failed`

### AT-004 under-evidenced entry fails closed

- acceptance target: `governance-check` rejects generic-subject entries that omit explicit bounded owner or verification evidence fields
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- required evidence: `missing bounded evidence rejection case`
- blocker taxonomy: `execution_pending_or_failed`

### AT-005 parseable-subject path does not regress

- acceptance target: existing parseable-subject backfill pass/reject cases continue to behave exactly as before after the new validation mode lands
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-check-protected-branch-merge-receipt-backfills`
- required evidence: `existing test matrix still green`
- blocker taxonomy: `execution_pending_or_failed`
