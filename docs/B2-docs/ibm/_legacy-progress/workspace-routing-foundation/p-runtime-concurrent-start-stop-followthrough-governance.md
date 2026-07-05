# Progress: runtime-concurrent-start-stop-followthrough-governance

- issue_id: `I-20260408-0231-A`
- issue_path: `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/issues/runtime-concurrent-start-stop-followthrough-governance.md`
- title: `Runtime concurrent start-stop followthrough governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-concurrent-start-stop-followthrough-20260411`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260411-feature-runtime-concurrent-start-stop-followthrough`
- updated_at: `2026-04-11`
- closure_status: `merged-and-verified`
- follow_on_to: `C-20260408-0231-A`

## Summary

This bounded owner carried the remaining runtime half of `C-20260408-0231-A` after canonical `develop` had already absorbed the generated-truth status half. Canonical `develop` now carries the runtime followthrough too.

## Implementation

- preserve same-project bootstrap attach during degraded process inspection
- clear stale project-scoped start locks before lawful startup
- stop every discovered same-project supervisor for the project
- preserve stop-marker truth until the last same-project supervisor exits

## Verification Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-start-cleans-stale-project-start-lock`
- `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-does-not-double-launch-during-degraded-starting-grace`
- `bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `bash docs/system/workspace/scripts/tests/test-freely-status-latest-generated-manager-continuity-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-semantic-loop-status-surface`
- `bash docs/system/workspace/scripts/tests/test-freely-restart-storm-status-surface`
- `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/code-reviews/20260411-runtime-concurrent-start-stop-followthrough-implementation-decision.md`
- `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/code-reviews/20260411-runtime-concurrent-start-stop-followthrough-verification.md`
- `docs/B2-docs/runtime/runtime-concurrent-start-stop-followthrough-governance/code-reviews/20260411-runtime-concurrent-start-stop-followthrough-canonical-closeout-verification.md`
- `develop` merge `bf7e5a16`

## Next Action

`completed`
