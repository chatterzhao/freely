# IBM Brainstorm - tasks-closeout-completion-and-adequacy-gate-governance

## Issue Link

- `docs/epics/workspace-routing-foundation/tasks-closeout-completion-and-adequacy-gate-governance/issues/tasks-closeout-completion-and-adequacy-gate-governance.md`

## Goal

Keep completion and guarded adequacy bound to one owner line by adding `tasks.md` closeout completeness to `pretests-gate` without demoting `pre-tests.md` from its verification-truth role.

## Constraints

1. `pretests-gate` remains the only owner-level completion and adequacy decision surface.
2. `governance-merge-gate` continues to inherit the behavior by delegation rather than parsing `tasks.md` itself.
3. The owner must fail closed when the bound `tasks.md` is missing or still unchecked.
4. Regression coverage must prove both direct gate behavior and inherited develop-merge behavior.

## Implementation Shape

1. Derive `tasks_path` from issue metadata when explicitly provided, else default to sibling `tasks.md` beside `pre-tests.md`.
2. Reuse existing source loading so staged-only and worktree-backed checks see the same file truth as the rest of `pretests-gate`.
3. Treat unchecked task boxes as a closeout blocker for:
   - `phase_state=completed`
   - `--require-adequacy`
4. Keep diagnostics narrow and owner-specific so operators see whether the blocker is missing `tasks.md` or unchecked tasks.

## Verification Shape

1. Add one regression where a completed owner still has unchecked tasks and must fail.
2. Add one regression where `--require-adequacy` hits the same blocker.
3. Keep `test-governance-merge-gate` aligned by staging a valid owner `tasks.md` and confirming no delegation regression.
