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
5. `freely live-status --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260327-200651-feature-start-restart-control-plane-semantics`

## Result

- `2026-03-30 16:12 PDT` develop absorption for the parent owner now exists at commit `b93efd2`, so this artifact remains in the diff only as continuity evidence tying `C-20260327-2006-A` to its already-merged parent before the downstream split owner `I-20260327-2006-A-global-restart` lands.
- `2026-03-30 15:47 PDT` manager-side rerun confirmed the focused regression still passes after a verification-lane test-harness hardening follow-up. The same command now completes in about `13.76s` instead of the previously observed ~`46s`, because the test no longer blocks command substitution on two background `sleep 30` probes. The same rerun also verified signal-aware cleanup: an `ALRM`-interrupted run now returns `142` and does not leave `ensure-interruption-dispatch --watch` residue under `/tmp/freely-project-command-semantics*`.
- `freely start` now reuses a healthy same-project supervisor, repairs stale local pid state, and avoids spawning a duplicate supervisor when project-safe discovery can recover the existing one.
- `freely restart` and `freely start --force` stay project-scoped: they wait for same-project child/supervisor shutdown, refuse stale foreign pid ownership, and do not escalate into implicit global reset.
- `freely restore-work` remains the explicit recovery surface for interrupted local AI work; project restart still does not silently restore work.
- Focused regressions now lock project-identity anchored process handling, sidecar readiness gates, attach/reuse hygiene, and same-project repair ordering.
- `governance-check` passes with only the repository's pre-existing legacy pre-brainstorm naming warnings.
- The implementation merge base remains checkpoint `5bc3a86`; the current worktree has stayed within the same issue lane for verification/writeback plus focused regression cleanup hardening, so the next lawful route is still manager-owned `completion_verification`, not a return to IBM or a jump to downstream global-restart work.

## Implementation Decision Note

- decision: legacy: completed verification artifact
- why_this: legacy: no detailed record
- alternatives_considered: legacy: no detailed record
- boundary_non_goals: legacy: no detailed record
- residual_risk: legacy: no detailed record
