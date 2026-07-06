# Brainstorm: cli-help-and-dry-run-contract-followthrough-governance

## Boundary

This owner only handles the remaining command-surface contract gaps from the canonical CLI replay:

1. explicit `--help` behavior for `wt-create`, `wt-enter`, `wt-add`, `pr-merge-guarded`, and top-level `freely`
2. a bounded dry-run result for `ai switch codex --dry-run --format json`

## Why This Is A Separate Lifecycle

- The completed packaging owner already repaired executable wrappers and `freely ai --help`, but it explicitly did not absorb broader help/dry-run semantics.
- `wt-create --help` is now a sharper defect than ordinary help noise because it reaches the create path and can attempt side effects.
- `ai switch codex --dry-run` is still a contract problem even when the underlying slot inventory is healthy, because automation cannot safely consume a dry-run path that performs the full probe flow.

## Initial Repair Direction

1. Add explicit top-level `--help|-h` handling before normal argument validation for the affected scripts.
2. Keep direct-exec rejection for sourced helpers, but let sourced `--help` succeed before branch logic.
3. Teach `ai-cli` dry-run auto-switch to summarize the saved-slot inventory immediately instead of running the long probe-and-switch path.
