# Pre-Tests: governance-merge-gate-review-aware-regression-alignment-governance

## Acceptance Targets

### AT-001 mixed unresolved-candidate fixture is review-aware

- acceptance target: the implementation-bearing mixed unresolved-candidate regression stages a complete owner review artifact and follows the current allowed path
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-merge-gate`
- required evidence: `focused regression`
- blocker taxonomy: `regression_missing`

### AT-002 same-file borrowed-owner bypass stays blocked

- acceptance target: directly touched same-file `promoted` / `absorbed` candidates still require their own canonical owner evidence and fail with the concrete owner diagnostic
- testing layer: focused regression
- target environment: `docs/system/workspace/scripts/tests/test-governance-merge-gate`
- required evidence: `focused regression`
- blocker taxonomy: `regression_missing`

### AT-003 closeout truth remains narrow

- acceptance target: completed lifecycle truth records the absorbed regression alignment without widening this owner into broader merge-gate policy redesign
- testing layer: governance
- target environment: issue/progress/milestone artifacts
- required evidence: `issue + progress + verification + governance-check`
- blocker taxonomy: `lifecycle_incomplete`

## Pre-merge acceptance

1. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
   - expectation: the mixed unresolved-candidate implementation case stages a complete review artifact and then passes, while same-file borrowed-owner regressions still fail
2. `git diff --check`
   - expectation: the refreshed fixture and lifecycle docs stay whitespace-clean
3. `./bin/governance-check`
   - expectation: the narrow reopen lifecycle is complete and merge-ready

## Post-merge acceptance

1. Canonical `develop` keeps `bash docs/system/workspace/scripts/tests/test-governance-merge-gate` green after replay.
2. The follow-on keeps merge-gate semantics aligned with existing law: unresolved metadata repairs remain allowed with same-line owner evidence, and same-file borrowed-owner regressions remain blocked.

## Acceptance Items

### AT-001
- id: `AT-001`
- requirement: `The mixed unresolved-candidate implementation regression stages review evidence and passes on the current allowed path.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/gate/governance-merge-gate-review-aware-regression-alignment-governance/code-reviews/20260404-governance-merge-gate-review-aware-regression-alignment-verification.md`

### AT-002
- id: `AT-002`
- requirement: `Same-file promoted or absorbed borrowed-owner regressions remain blocked by canonical owner binding.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/gate/governance-merge-gate-review-aware-regression-alignment-governance/code-reviews/20260404-governance-merge-gate-review-aware-regression-alignment-verification.md`

### AT-003
- id: `AT-003`
- requirement: `The closeout lane keeps this owner completed and bounded on canonical develop.`
- evidence_level: `integration`
- status: `pass`
- artifact_ref: `docs/B2-docs/gate/governance-merge-gate-review-aware-regression-alignment-governance/code-reviews/20260404-governance-merge-gate-review-aware-regression-alignment-verification.md`
