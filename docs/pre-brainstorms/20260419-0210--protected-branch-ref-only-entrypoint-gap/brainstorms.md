# Brainstorms - 20260419-0210--protected-branch-ref-only-entrypoint-gap

- date: `2026-04-19`
- status: `pre-brainstorm`
- source: `real protected-root merge replay`

## Context

Canonical `develop` was advanced locally with `git merge --ff-only feature/runtime-startup-self-healing-boundary-20260419` from the protected-root worktree. That update did not trigger `pre-merge-commit`, because no merge commit was created. The branch only hit governance enforcement later at `git push origin develop`.

The result is a narrower but real protected-branch gap:

1. The repository claims `freely pr-merge-guarded` is the canonical protected-merge entrypoint.
2. Existing `pre-merge-commit` enforcement only covers merge-commit creation and merge completion.
3. Git still permits ref-only protected-branch advances such as `git merge --ff-only ...` before push-time gates run.
4. This lets protected-root local truth drift away from the declared entrypoint contract even when push is eventually blocked or later succeeds.

## Why Existing Owners Do Not Fully Absorb This

`develop-guarded-merge-entrypoint-enforcement-governance` closed the merge-commit path correctly, but its implementation boundary was explicitly `pre-merge-commit`. That owner never claimed to intercept protected-branch ref transactions that skip merge-commit creation entirely.

This follow-on is therefore narrower than a full protected-merge redesign:

1. do not reopen receipt policy,
2. do not reopen server-side enforcement,
3. do not widen into generic push governance,
4. only close the local protected-branch ref-only entrypoint hole that left `ff-only` outside the canonical guarded path.

## Proposed Boundary

Freeze one explicit rule:

1. Protected branch refs (`main`, `develop`, `test-pre-merge-*`) may advance only to a canonical receipt-bearing protected merge commit.
2. Ref-only updates that move a protected branch to a non-receipted commit must fail before the ref is written.
3. Receipt-bearing protected merge commits must remain valid, including the existing guarded merge path.

## Candidate Repair Direction

The cleanest local enforcement point is `reference-transaction`:

1. it observes protected-branch ref updates even when `pre-merge-commit` never runs,
2. it can fail the ref update before the branch actually moves,
3. it avoids post-merge rollback hacks,
4. it is not bypassed by `--no-verify`, which makes it materially stronger than the current merge-only hook path.

## Success Criteria For This Research Slice

This pre-brainstorm is complete only if it freezes:

1. why `ff-only` is a real protected-branch policy gap rather than only a delayed push-time inconvenience,
2. why `reference-transaction` is the narrowest correct local gate,
3. why the repair should accept receipt-bearing merge commits but reject non-receipted protected-branch ref advances,
4. why this is a follow-on to the earlier develop entrypoint owner instead of a reopen of its completed scope.
