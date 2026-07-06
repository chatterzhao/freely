# Brainstorm: protected-merge-unparseable-subject-receipt-gap-governance

## Decision Snapshot

- Keep the owner narrow: it only covers trailerless protected-ancestry merges whose subjects are too generic to validate against the current subject-matched receipt-gap contract.
- Preserve fail-closed semantics: the new path must require stronger explicit evidence, not looser matching.
- Preferred implementation direction: add an explicit validation mode inside `docs/system/workspace/hooks/protected-branch-merge-receipt-backfills.md` instead of silently overloading the current entry shape.

## Proposed Schema

- `validation_mode: unparseable_subject_ancestry`
- `protected_batch_branch`
- `absorbing_protected_merge`
- `bounded_issue`
- `verification_ref`

The existing fields remain required unless implementation proves a cleaner split is necessary:
- `target_branch`
- `canonical_merge_path`
- `canonical_bypass_mode`

## Required Invariants

1. `absorbing_protected_merge` must be a trailer-bearing protected merge on the scanned branch.
2. The absorbing merge's `Freely-Source-Branch` must equal `protected_batch_branch`.
3. The claimed unparseable merge commit must be reachable in the absorbed ancestry segment below `absorbing_protected_merge`.
4. `bounded_issue` and `verification_ref` must point at the same bounded owner family that produced the protected batch.
5. Parseable-subject merges must stay on the old contract and be rejected if they try to use the new validation mode.

## Rejection Priorities

1. Missing `validation_mode` for a generic-subject ancestry entry.
2. Missing or trailerless `absorbing_protected_merge`.
3. `protected_batch_branch` mismatch against the absorbing merge trailer.
4. Claimed merge hash not actually part of the absorbed ancestry chain.
5. Generic free-text evidence with no explicit bounded owner and verification fields.
