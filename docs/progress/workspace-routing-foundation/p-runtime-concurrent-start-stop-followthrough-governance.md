# Progress: runtime-concurrent-start-stop-followthrough-governance

- issue_id: `I-20260408-0231-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-concurrent-start-stop-followthrough-governance/issues/runtime-concurrent-start-stop-followthrough-governance.md`
- title: `Runtime concurrent start-stop followthrough governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-concurrent-start-stop-followthrough-20260411`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260411-feature-runtime-concurrent-start-stop-followthrough`
- updated_at: `2026-04-11`
- follow_on_to: `C-20260408-0231-A`

## Summary

This bounded owner carries the still-unmerged runtime half of `C-20260408-0231-A` after canonical `develop` already absorbed the generated-truth status half.

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
- `docs/epics/workspace-routing-foundation/runtime-concurrent-start-stop-followthrough-governance/code-reviews/20260411-runtime-concurrent-start-stop-followthrough-implementation-decision.md`
- `docs/epics/workspace-routing-foundation/runtime-concurrent-start-stop-followthrough-governance/code-reviews/20260411-runtime-concurrent-start-stop-followthrough-verification.md`
- Git commit `c770aeac` on this feature branch

## Next Action

Merge to `develop` through a guarded `test-pre-merge-*` batch.
