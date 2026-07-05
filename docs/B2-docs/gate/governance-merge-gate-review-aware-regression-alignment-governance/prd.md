# PRD: governance-merge-gate-review-aware-regression-alignment-governance

## Goal

Keep `test-governance-merge-gate` aligned with the canonical merge-gate contract by making the mixed unresolved-candidate implementation regression review-aware.

## Product Requirement

1. The mixed unresolved-candidate implementation fixture must stage a valid owner review artifact before it asserts the current allowed path.
2. Same-file `promoted` / `absorbed` candidates must not bypass canonical owner binding just because another touched owner candidate lives in the same `candidates.md`.
3. The regression must reflect the canonical rule that unresolved `proposed|needs_research|blocked` candidate metadata repairs may travel with same-line governance owner evidence.
4. No merge-gate policy or wording widening is allowed in this lane.
