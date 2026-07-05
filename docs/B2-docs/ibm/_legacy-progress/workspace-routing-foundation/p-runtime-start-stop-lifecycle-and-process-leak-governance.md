# Progress: runtime-start-stop-lifecycle-and-process-leak-governance

- issue_id: `I-20260417-0445-A`
- issue_path: `docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/issues/runtime-start-stop-lifecycle-and-process-leak-governance.md`
- title: `Runtime start/stop lifecycle and process leak governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-process-leak-20260417`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260417-integration-runtime-lifecycle-worker`
- updated_at: `2026-04-18`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- The owner is now fully materialized from `C-20260417-0445-A` as the bounded runtime implementation slice that freezes CLI-first repeated-start rejection, lawful start-lock handling, discovered relauncher cleanup, AI fast-exit containment, and lifecycle-trace support for the same seam.
- Focused premerge-integration regressions already passed on `test-pre-merge-runtime-lifecycle-20260417`, so the remaining blocker was governance lifecycle truth rather than executable evidence.
- The next lifecycle step is to replay the guarded `test-pre-merge-* -> develop` promotion once this issue/progress/pre-tests/review chain is in place.

## Verification Evidence

1. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-daemon-start-precheck-ignores-self-owned-start-lock`
2. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-daemon-start-rejects-when-runtime-already-running`
3. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-daemon-start-releases-start-lock-when-launch-fails`
4. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-interruption-manager-fast-path-control-validation`
5. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-lifecycle-trace-log`
6. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-lock-cleans-stalled-active-owner`
7. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-orphaned-ai-pid`
8. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-precheck-ignores-self-owned-start-lock`
9. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-rejects-when-runtime-already-running`
10. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-start-releases-start-lock-when-startup-fails`
11. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-discovered-watchers-and-dispatchers`
12. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-detects-codex-session-permission-failure`
13. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-detects-fast-exit-iflow-local-state-failure`
14. `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-monitor-ai-cli-kills-iflow-descendants-on-runtime-failure`
15. `./bin/test-lane premerge-integration -- ./bin/governance-check`
16. `git diff --check`
17. `docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-verification.md`
18. `docs/B2-docs/runtime/runtime-start-stop-lifecycle-and-process-leak-governance/code-reviews/20260418-runtime-start-stop-lifecycle-and-process-leak-closeout-verification.md`

## Current Batch Risks

1. The remaining promote blocker is governance-chain completeness and guarded develop replay, not missing focused regressions.
2. Canonical `develop` still needs one short post-merge followthrough replay before this owner can be retired.
3. The sibling lifecycle-trace feature lane remains separate work and must not be silently absorbed into this owner during cleanup.

## Next Action

1. Update candidate and milestone truth so `I-20260417-0445-A` is the canonical owner bound to `C-20260417-0445-A`.
2. Re-run `./bin/governance-check` in the source writable worktree.
3. Replay `freely pr-merge-guarded develop test-pre-merge-runtime-lifecycle-20260417`, then run the canonical `develop` followthrough and retire the disposable `test-pre-merge-*` worktree.

## Closeout

- completed_at: `2026-04-28`
- merge_evidence: `merged via 903537ad (feature/runtime-process-leak-20260417)`
