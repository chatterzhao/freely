# Progress: foreground-background-runtime-entrypoint-semantics-governance

- issue_id: `I-20260413-0208-A`
- issue_path: `docs/B2-docs/ibm/foreground-background-runtime-entrypoint-semantics-governance/issues/foreground-background-runtime-entrypoint-semantics-governance.md`
- title: `Foreground/background runtime entrypoint semantics governance`
- phase_state: `completed`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-daemon-semantics-closeout-20260413`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260413-feature-runtime-daemon-semantics-closeout`
- updated_at: `2026-04-13`
- closure_status: `merged-and-verified`

## Summary

This owner is now closed on canonical `develop`:

- Freely keeps `start/restart/stop/status` on the existing foreground contract
- Freely now exposes explicit `daemon start|stop|status|logs` for detached runtime ownership
- the same runtime truth continues to feed `live-status` and daemon observability
- guarded premerge promotion, develop merge, push followthrough, and temporary worktree retirement all completed on `2026-04-13`

## Implementation

- added `freely daemon start|stop|status|logs` as the explicit background runtime control surface
- preserved the existing foreground contract by keeping `start` and `restart` on `entrypoint_mode=foreground`
- taught supervisor discovery and same-project ownership checks to recognize both foreground and daemon entrypoints against the same project runtime truth
- recorded `entrypoint_mode` in supervisor runtime events so detached daemon starts are distinguishable from foreground launches without introducing a second state family
- added focused daemon regressions for command routing, detached persistence after launcher return, explicit stop semantics, and shared `live-status` truth

## Verification Evidence

- `develop` merge `1b55aae6`
- `premerge` merge `d9dc3167`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-command-semantics`
- `bash docs/system/workspace/scripts/tests/test-freely-daemon-runtime-detach-and-shared-status`
- `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
- `bash docs/system/workspace/scripts/tests/test-freely-runtime-supervisor-event-log`
- `bash docs/system/workspace/scripts/tests/test-freely-stop-terminates-all-same-project-supervisors`
- `./bin/governance-check`
- `docs/B2-docs/ibm/foreground-background-runtime-entrypoint-semantics-governance/code-reviews/20260413-foreground-background-runtime-entrypoint-semantics-verification.md`
- `docs/B2-docs/ibm/foreground-background-runtime-entrypoint-semantics-governance/code-reviews/20260413-foreground-background-runtime-entrypoint-semantics-closeout-verification.md`

## Closure Evidence

1. `develop` merge `1b55aae6`
2. `docs/B2-docs/ibm/foreground-background-runtime-entrypoint-semantics-governance/code-reviews/20260413-foreground-background-runtime-entrypoint-semantics-verification.md`
3. `docs/B2-docs/ibm/foreground-background-runtime-entrypoint-semantics-governance/code-reviews/20260413-foreground-background-runtime-entrypoint-semantics-closeout-verification.md`

## Next Action

1. No further action in this owner unless canonical `develop` loses the explicit daemon control-plane contract or foreground `start` semantics drift.
2. Any future daemon restart policy, UI/TUI attach behavior, or broader command-surface redesign should reopen as a new bounded owner instead of reviving this completed record.
