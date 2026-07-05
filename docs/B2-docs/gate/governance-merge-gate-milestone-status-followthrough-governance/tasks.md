# Tasks: governance-merge-gate-milestone-status-followthrough-governance

## Slice 1: Owner materialization

- [x] Materialize a new narrow followthrough instead of mutating the completed protected-branch merge receipt hardening owner.
- [x] Record the reopen source and keep the scope parser-bound.
- [x] Carry same-line candidate, issue, progress, and review evidence.

## Slice 2: Parser repair

- [x] Restrict milestone status parsing to milestone-level fields.
- [x] Preserve existing queue item parsing for issue paths and source candidates.
- [x] Avoid widening active-candidate placement semantics.

## Slice 3: Regression

- [x] Add a replay-shaped fixture where the milestone is `active` but a nested candidate item is `needs_research`.
- [x] Prove `governance-merge-gate --staged` still passes that valid active-milestone lifecycle line.
- [x] Re-run `git diff --check` and `./bin/governance-check`.
