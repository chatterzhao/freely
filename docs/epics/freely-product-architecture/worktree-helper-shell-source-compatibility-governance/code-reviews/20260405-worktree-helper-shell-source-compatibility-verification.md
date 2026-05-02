# Verification: worktree-helper-shell-source-compatibility-governance

- issue_id: `I-20260405-2302-A`
- verified_on: `2026-04-05`
- canonical_branch: `develop`
- canonical_merge_commit: `3e0c8b9`
- verification_owner: `codex`

## Verified Commands

- `zsh -lc 'source ./bin/wt-add -- README.md'`
- `zsh -lc 'source ./bin/wt-enter develop'`
- `bash -lc 'source ./bin/wt-add -- README.md'`
- `bash -lc 'source ./bin/wt-enter develop'`
- `./bin/wt-add -- README.md`
- `./bin/wt-enter develop`

## Verified Lanes

- `./bin/test-lane feature-local -- ./bin/governance-check`
- `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-wt-wrapper-shell-source-compatibility`
- `./bin/test-lane feature-local -- bash docs/system/workspace/scripts/tests/test-worktree-entry-flow`
- `./bin/test-lane premerge-integration -- ./bin/governance-check`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-wt-wrapper-shell-source-compatibility`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-worktree-entry-flow`
- `./bin/test-lane post-merge-followthrough -- ./bin/governance-check`
- `./bin/test-lane post-merge-followthrough -- bash docs/system/workspace/scripts/tests/test-wt-wrapper-shell-source-compatibility`
- `./bin/test-lane post-merge-followthrough -- bash docs/system/workspace/scripts/tests/test-worktree-entry-flow`

## Outcome

- Canonical `develop` now preserves the documented `source ./bin/wt-add ...` and `source ./bin/wt-enter ...` contract under both `bash` and default `zsh`.
- `wt-add` still rejects direct execution and still blocks protected or `test-pre-merge-*` branches.
- `wt-enter` still enters existing worktrees and still materializes dated worktree paths with the timestamp-first naming policy.
