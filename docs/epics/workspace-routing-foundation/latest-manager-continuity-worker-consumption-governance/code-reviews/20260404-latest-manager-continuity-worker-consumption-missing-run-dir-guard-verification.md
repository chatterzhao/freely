# Code Review: latest-manager-continuity-worker-consumption-governance missing-run-dir guard verification

- issue_id: `I-20260322-0445`
- review_scope: `same-family guard for sibling worktrees that lack .freely/run during live-status and fleet-status scans`
- verdict: `pass_with_scope_limits`

## Findings

1. Shared helper functions in `docs/system/workspace/scripts/runtime/freely` now short-circuit when sibling runtime or logs directories are absent, so status scans no longer emit `find` stderr for uninitialized worktrees.
2. The focused regression `test-freely-status-silences-missing-sibling-run-dir` now asserts empty stderr separately for `live-status` and `fleet-status`, which is stronger than matching one warning string.
3. The semantic-loop regression now also carries a sibling worktree without `.freely/run`, so the monitoring path that consumes `manager_semantic_loop_repeat_state_for_project()` no longer leaks missing-directory stderr before it reaches the pre-existing active-worker assertion.
4. Existing status-family regressions still pass, so the guard does not regress ordinary continuity, prompt, or fleet reporting.

## Verification Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-status-silences-missing-sibling-run-dir`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `bash docs/system/workspace/scripts/tests/test-freely-fleet-status`
- `freely fleet-status --project /Users/zhaoyu/Downloads/code/my-freely/freely`
- `./bin/governance-check`

## Residual Risk

1. This verifies the current shared `.freely/run` helper family only; unrelated future scans that bypass these helpers could still leak path-missing stderr.
2. The broader runtime supervision candidate around websocket denial, slot-switch busy, and blocked intake truth remains unresolved by this fix.
3. `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface` still fails at the old `semantic loop signal should clear when a worker is already running` assertion on both this branch and unchanged `develop`; the new missing-run-dir guard removes stderr noise before that point, but does not resolve the pre-existing active-worker detection gap.
4. `./bin/governance-check` in this worktree still reports the repository's two pre-existing protected-branch merge receipt gaps on `develop` (`6969be7e02ea0c380a9e9fc892b5184168d261fb`, `9fa8ec35bb9532235bd8cb51b6e20c6730836d7c`), not a lane-local regression.
