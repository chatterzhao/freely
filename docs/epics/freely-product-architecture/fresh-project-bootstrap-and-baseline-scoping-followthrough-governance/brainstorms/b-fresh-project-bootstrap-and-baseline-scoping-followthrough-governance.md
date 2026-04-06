# Brainstorm: fresh-project-bootstrap-and-baseline-scoping-followthrough-governance

## Current Narrowing

The root bug is not “fresh-project bootstrap is generally broken”. The narrower truth is:

1. `sync-tooling` already knows how to rematerialize managed tool-local surfaces, but it currently copies source config absolute paths without retargeting them.
2. That makes `baseline-status` and `status --view baseline` look wrong even though the command is pointed at a different project.
3. Fresh projects also miss `.githooks`, so `init` still hits the hook gate before it can write corrected target-local config.

## Decision

Keep the repair in one owner because the two defects share one first-hop boundary:

- `sync-tooling` is the handoff point from an existing authoritative project to a fresh git target.
- The wrong config copy and the missing hook surface both happen there.
- The acceptance proof should be one real replay: sync into a fresh project, inspect baseline/status, run `init`, and confirm the target project stays authoritative.

## Adjacent Guards

1. `ensure-interruption-dispatch --project <x>` stays only as a non-regression check that doc gate failure is semantic.
2. `I-20260405-1235-A` remains the upper-bound authorization/bootstrap architecture owner.
3. `I-20260403-2041-A` remains the earlier worktree boundary/bootstrap owner; this lane is a followthrough on fresh-project retargeting, not a reopen of sibling-worktree policy.
