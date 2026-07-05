# Brainstorms - 20260413-1640--tasks-closeout-completion-and-adequacy-gate

## Context

`I-20260413T042000Z-B` and `I-20260413T042000Z-C` were already recorded as completed in milestone, issue, progress, branch, and worktree truth, but their sibling `tasks.md` files still carried unchecked closeout boxes.

The current guarded `develop` replay for `feature/tasks-closeout-gate-20260413` also proved the remaining implementation gap is not in merge orchestration itself. The missing contract is narrower: `pretests-gate` already treats `pre-tests.md` as verification truth for completion and guarded promote, but it did not scan `tasks.md` as execution closeout truth before allowing `completed` or `--require-adequacy` verdicts.

## Trigger

This follow-on started from a real owner audit, not from hypothetical schema cleanup:

1. `I-20260413T042000Z-B` and `I-20260413T042000Z-C` showed `phase_state=completed` while their `tasks.md` still had unchecked closeout items.
2. The real fix belongs in `pretests-gate`, because `governance-merge-gate` already delegates owner-bound adequacy to that gate.
3. A guarded `test-pre-merge-* -> develop` replay then blocked on missing owner lifecycle evidence, proving the narrow code fix must be paired with a lawful candidate/issue/progress/review chain before upstream merge can complete.

## Verified Repo Facts

1. `docs/system/workspace/scripts/quality/pretests-gate` already loads issue-bound `pre-tests.md` and is the canonical place where completion and `--require-adequacy` are decided.
2. `docs/system/workspace/scripts/quality/governance-merge-gate` delegates develop-bound owner verification to `pretests-gate`; duplicating `tasks.md` parsing there would create a second closeout truth path.
3. `I-20260413T042000Z-B` and `I-20260413T042000Z-C` each retained unchecked `tasks.md` lines even after milestone and progress closeout had been written back.
4. The implemented fix can stay narrow: derive a sibling `tasks.md` path from the bound owner, fail closed when the file is missing during completion or adequacy checks, and reject any remaining unchecked task boxes.

## Boundary

This follow-on only:

1. Binds `tasks.md` into `pretests-gate` as closeout-completeness truth for `phase_state=completed` and guarded adequacy paths.
2. Adds regression coverage for direct `pretests-gate` failure and inherited `governance-merge-gate` behavior.
3. Records the lawful lifecycle evidence needed for this already-implemented repair to merge into canonical `develop`.

This follow-on does not:

1. Redesign `pre-tests.md` as the verification truth source.
2. Add a new parallel ledger beside `tasks.md` and `pre-tests.md`.
3. Move `tasks.md` parsing into `governance-merge-gate`.
4. Reopen unrelated startup-routing owners beyond citing the audit that exposed this residual gap.

## Working Conclusion

Materialize one narrow workspace-routing-foundation owner that treats `tasks.md` as execution closeout truth inside `pretests-gate`, keeps `pre-tests.md` as the only verification truth, proves the behavior through focused regressions, and supplies the candidate-driven lifecycle evidence required for guarded upstream merge.
