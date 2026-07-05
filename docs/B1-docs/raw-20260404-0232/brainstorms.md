# Brainstorms - 20260404-0232--governance-merge-gate-review-aware-regression-alignment

## Context

Canonical `develop` post-merge acceptance reran `bash docs/system/workspace/scripts/tests/test-governance-merge-gate` and exposed a narrow regression in the test fixture rather than in `governance-merge-gate` itself.

## Trigger

The failing case (`stdout2d`) still expected a negative result, but current canonical policy no longer blocks that mixed diff once review evidence is present.

The fixture touches:

- an unresolved `needs_research` candidate metadata repair
- milestone queue metadata
- same-line owner progress evidence
- an implementation-bearing file

After `I-20260401-2354-A`, implementation-bearing diffs must also stage an owner review artifact. Once that review artifact is present, current policy intentionally allows unresolved `proposed|needs_research|blocked` candidate metadata repairs to travel inside the same governance owner line.

## Verified Repo Facts

1. `docs/system/workspace/scripts/tests/test-governance-merge-gate` case `2d` predates `I-20260401-2354-A` and never stages a review artifact for the same-line owner.
2. `docs/epics/workspace-routing-foundation/active-milestone-placement-and-consumption-gate-governance/code-reviews/20260331-active-milestone-placement-gate-verification.md` already records the newer rule: unresolved `proposed|needs_research|blocked` candidate metadata repairs may travel inside the current governance owner while the same merge carries issue/progress/review evidence.
3. Reproducing the current path shows `stdout2d` becomes `Develop merge governance gate passed.` once the staged review artifact is added.
4. The same inspection also exposed a real file-scope bypass: directly touched `promoted` / `absorbed` candidates could share a `candidates.md` file with the true owner candidate and incorrectly skip owner-binding validation.
5. The follow-on therefore needs both a review-aware fixture refresh for the allowed unresolved-candidate case and a narrow gate repair for same-file borrowed-owner regressions.

## Boundary

This follow-on only:

1. Reopens the regression fixture so implementation-bearing unresolved-candidate coverage stages a valid owner review artifact first.
2. Restores owner-binding enforcement for same-file `promoted` / `absorbed` borrowed-owner scenarios.
3. Keeps `test-governance-merge-gate` aligned with the current merge-gate contract without widening enforcement.
4. Records the new same-line lifecycle needed for this post-merge acceptance finding.

This follow-on does not:

1. Redesign `governance-merge-gate` owner-resolution policy.
2. Relax staged review artifact requirements for implementation-bearing merges.
3. Reopen broader merge-gate parser, milestone, or protected-branch receipt work.

## Working Conclusion

Materialize a narrow workspace-routing-foundation owner that refreshes the mixed unresolved-candidate regression fixture, removes the same-file borrowed-owner bypass, reruns `test-governance-merge-gate`, and keeps the gate contract aligned with existing milestone and owner-binding law.
