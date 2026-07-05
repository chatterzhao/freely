# Verification: pretests-adequacy-item-schema-materialization-governance

- issue_id: `I-20260411-1415-A`
- issue_path: `docs/B2-docs/gate/pretests-adequacy-item-schema-materialization-governance/issues/pretests-adequacy-item-schema-materialization-governance.md`
- verification_date: `2026-04-12`
- verifier: `codex`

## Scope Verdict

- `PASS`: `pretests-gate` now requires at least one adequacy-v2 Acceptance Item for the targeted lane/gate pair instead of letting develop-bound adequacy pass with legacy-only items.
- `PASS`: staged `test-pre-merge-* -> develop` promote now requires a fresh staged review artifact under the owner-bound `verification_artifact_dir`, so reused committed artifacts no longer satisfy guarded completion.
- `PASS`: `governance-merge-gate` now rejects overly broad `verification_artifact_dir` values and only accepts canonical `docs/epics/.../code-reviews` ownership.
- `PASS`: IBM/doc truth now teaches new owners to write adequacy-v2 fields instead of leaving schema uptake implicit.
- `PASS`: the guarded `pre-merge-commit` hook path was replayed end-to-end, including the docs-only promote case where owner `pre-tests.md` stays pending until adequacy evidence is staged.
- `PASS`: a disposable `test-pre-merge-20260411-pretests-adequacy-closeout` batch, assembled through `pr-merge-guarded`, passed `premerge-integration` checks and exposed the missing `premerge-integration:develop_merge` adequacy statement that is now materialized in the owner `pre-tests.md`.
- `PASS`: this owner now explicitly carries the absorbed follow-on provenance for `C-20260411-1414-B`, keeping the launch-time hard-gate brainstorm and the adequacy-v2 owner linked without reopening a parallel launch-time issue.
- `PASS`: canonical owner/progress closeout text now reflects that this adequacy-v2 lane is already merged and retired, so future review and routing logic do not misclassify it as an active promote candidate.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-pretests-gate`
2. `bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
3. `bash docs/system/workspace/scripts/tests/test-pre-merge-commit-hook`
4. `./bin/governance-check`
5. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-pretests-gate`
6. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-governance-merge-gate`
7. `./bin/test-lane premerge-integration -- ./bin/governance-check`
8. `freely pr-merge-guarded test-pre-merge-20260412-completed-owner-closeout-truth feature/completed-owner-closeout-truth-20260412`

## Implementation Decision Note

- decision: `Materialize adequacy-v2 as issue-owned Acceptance Item metadata and make guarded develop promote consume it directly, rather than inferring sufficiency from generic pass items or review-path heuristics.`
- why_this: `The observed gate miss was not that pre-tests existed in the abstract, but that develop-bound promote could still pass without a machine-readable statement of which lane/gate pair had been sufficiently covered by fresh owner-scoped evidence.`
- alternatives_considered: `Keep adequacy semantics in prose only; trust any artifact-backed pass item; allow broad verification directories; leave hook coverage on the old fixture shape.`
- boundary_non_goals: `This owner does not harden launch-time verification contract enforcement, cleanup/retirement gates, or force a warehouse-wide migration of historical pre-tests.`
- residual_risk: `Older owners still rely on legacy compatibility until they adopt adequacy-v2 fields, and guarded promote still depends on operators replaying both adequacy statements and fresh staged review evidence back into the canonical owner lane before final develop merge.`
