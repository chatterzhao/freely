# Brainstorm: worktree-helper-shell-source-compatibility-governance

## Framing

- This owner is a narrow follow-on to `worktree-tool-boundary-bootstrap-governance`, not a reopen of its broader tooling-boundary contract.
- The concrete regression is on the documented `bin/` wrapper path under default `zsh`.

## Decision

1. Keep `wt-create` as the standard path.
2. Preserve `wt-add` / `wt-enter` as documented convenience helpers.
3. Make the `bin/` wrappers source-safe in the default shell context instead of requiring operators to manually switch to `bash`.
4. Add focused regressions that exercise the actual documented wrapper commands.

## Boundary

1. Do not widen into a generic wrapper framework rewrite.
2. Do not redesign the worktree contract or protected-branch rules.
3. Only absorb additional sourced wrappers if the same bug is proven with direct evidence in this lane.
