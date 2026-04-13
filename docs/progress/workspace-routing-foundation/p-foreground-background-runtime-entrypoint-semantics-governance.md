# Progress: foreground-background-runtime-entrypoint-semantics-governance

- issue_id: `I-20260413-0208-A`
- issue_path: `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/issues/foreground-background-runtime-entrypoint-semantics-governance.md`
- title: `Foreground/background runtime entrypoint semantics governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-daemon-semantics`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/feature-runtime-daemon-semantics`
- updated_at: `2026-04-13`

## Summary

This owner has now moved past IBM into feature-local implementation and verification: Freely keeps `start/restart/stop/status` on the existing foreground contract while adding an explicit `daemon` control plane for detached runtime ownership.

## Implementation

- added `freely daemon start|stop|status|logs` as the explicit background runtime control surface
- preserved the existing foreground contract by keeping `start` and `restart` on `entrypoint_mode=foreground`
- taught supervisor discovery and same-project ownership checks to recognize both foreground and daemon entrypoints against the same project runtime truth
- recorded `entrypoint_mode` in supervisor runtime events so detached daemon starts are distinguishable from foreground launches without introducing a second state family
- added focused daemon regressions for command routing, detached persistence after launcher return, explicit stop semantics, and shared `live-status` truth

## Verification Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-daemon-command-semantics`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `bash docs/system/workspace/scripts/tests/test-freely-runtime-supervisor-event-log`
- `bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
- `./bin/governance-check`
- `docs/epics/workspace-routing-foundation/foreground-background-runtime-entrypoint-semantics-governance/code-reviews/20260413-foreground-background-runtime-entrypoint-semantics-verification.md`

## Next Action

Promote through a dedicated `test-pre-merge-*` lane, then merge to `develop` and rewrite the owner to canonical `completed` truth.
