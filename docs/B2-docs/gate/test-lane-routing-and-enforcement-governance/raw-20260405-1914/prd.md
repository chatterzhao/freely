# PRD: test-lane-routing-and-enforcement-governance

## Goal

Make test execution lanes explicit, machine-enforced, and aligned with Freely's branch/worktree governance.

## Product Requirement

1. Freely must expose one explicit wrapper entrypoint for lane selection: `./bin/test-lane`.
2. Freely must keep three canonical lanes:
   - `feature-local`
   - `premerge-integration`
   - `post-merge-followthrough`
3. Freely must map `feature-local` only to dedicated `feature/*`, `feature/premerge-*`, `release/*`, and `hotfix/*` worktrees.
4. Freely must reject lane/branch mismatches instead of silently running anyway.
5. Freely must keep wrapper entrypoints directly executable, not only `bash`-invokable.
6. Freely must align related skills and references with the current `test-pre-merge-* -> develop` promote model.
