# Verification: project-command-semantics-and-restore-work-governance

- issue_id: `I-20260327-2006-A`
- verification_scope: feature-lane verification before manager-owned completion closeout
- verified_in_worktree: `feature/start-restart-control-plane-semantics-20260327-200651`
- checkpoint_commit: `5bc3a86`

## Commands

1. `bash -n docs/system/workspace/scripts/runtime/freely`
2. `bash docs/system/workspace/scripts/tests/test-freely-project-command-semantics`
3. `bash docs/system/workspace/scripts/tests/test-freely-start-requires-interruption-dispatcher-ready`
4. `./bin/governance-check`
5. `./bin/freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260327-200651-feature-start-restart-control-plane-semantics`

## Result

- `freely start` now reuses a healthy same-project supervisor, repairs stale local pid state, and avoids spawning a duplicate supervisor when project-safe discovery can recover the existing one.
- `freely restart` and `freely start --force` stay project-scoped: they wait for same-project child/supervisor shutdown, refuse stale foreign pid ownership, and do not escalate into implicit global reset.
- `freely restore-work` remains the explicit recovery surface for interrupted local AI work; project restart still does not silently restore work.
- Focused regressions now lock project-identity anchored process handling, sidecar readiness gates, attach/reuse hygiene, and same-project repair ordering.
- `governance-check` passes with only the repository's pre-existing legacy pre-brainstorm naming warnings.
- The feature lane is checkpointed and clean at `5bc3a86`, so the next lawful route is manager-owned `completion_verification`, not a return to IBM or further dev expansion in this worktree.
