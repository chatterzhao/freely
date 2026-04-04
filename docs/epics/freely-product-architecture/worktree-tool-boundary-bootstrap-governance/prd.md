# PRD: worktree-tool-boundary-bootstrap-governance

## Goal

Make Freely's managed tool boundary contract survive the move from the project root into sibling worktrees.

## User/Operator Outcome

- New worktrees automatically regain the same managed local tool boundary surfaces the project root already has.
- Tools that need an explicit writable-root extension can work in `{project}-worktrees` without pushing implementation back into protected roots.
- Project root remains valid for bootstrap, read, merge, and integration work.

## Constraints

- No umbrella reopen.
- No fake project-local config surfaces for unsupported tools.
- Manual `git worktree add` remains allowed only as fallback plus immediate `freely sync-tooling`.
