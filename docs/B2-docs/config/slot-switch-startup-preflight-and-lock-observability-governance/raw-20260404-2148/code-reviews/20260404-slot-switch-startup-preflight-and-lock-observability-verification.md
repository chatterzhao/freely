# Verification: slot-switch-startup-preflight-and-lock-observability-governance

- issue_id: `I-20260404-2148-A`
- issue_path: `docs/B2-docs/config/slot-switch-startup-preflight-and-lock-observability-governance/issues/slot-switch-startup-preflight-and-lock-observability-governance.md`
- branch: `feature/slot-switch-startup-preflight-governance-20260404-2138`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260404-2138-feature-slot-switch-startup-preflight-governance`
- verification_date: `2026-04-04`
- title: `Slot-switch startup preflight and lock observability governance`
- verifier: `codex`
- scope: bounded startup preflight plus current lock observability for the shared codex slot-switch lock
- verdict: `pass_for_verification`

## Summary

- Root evidence replay confirmed the latest startup failure is still `auth_failure`, not a currently active shared lock, so this owner stayed narrow instead of reopening blocked-intake supervision.
- `docs/system/workspace/scripts/runtime/freely` now snapshots the shared slot-switch lock into explicit `idle | active | stale | ambiguous` states and uses that same truth for startup and reporting.
- `freely start` now auto-cleans only `stale`, bounded-waits on `active`, and fails closed on `ambiguous` without leaking raw `sed` stderr as the only diagnosis surface.
- `doctor`, `baseline-status`, and `live-status` now expose the same `current_slot_switch_lock_*` fields for operator-visible diagnosis.

## Implementation Decision Note

- see `docs/B2-docs/config/slot-switch-startup-preflight-and-lock-observability-governance/raw-20260404-2148/code-reviews/20260404-slot-switch-startup-preflight-and-lock-observability-implementation-decision.md`

## Verification

1. `bash -n docs/system/workspace/scripts/runtime/freely`
2. `bash docs/system/workspace/scripts/tests/test-freely-start-cleans-stale-slot-switch-lock`
3. `bash docs/system/workspace/scripts/tests/test-freely-start-times-out-on-active-slot-switch-lock`
4. `bash docs/system/workspace/scripts/tests/test-freely-slot-switch-lock-status-surface`
5. `bash docs/system/workspace/scripts/tests/test-freely-status-family`
6. `./bin/governance-check`

## Findings

- No finding: startup now removes stale shared locks and proceeds without manual filesystem cleanup.
- No finding: active shared locks remain non-destructive and fail clearly after the configured bounded wait.
- No finding: malformed or missing lock state now produces structured `ambiguous`/detail output on doctor and status surfaces instead of raw parser noise.

## Residual Risks

- Canonical root startup can still fail for `auth_failure`; this owner only ensures slot-switch lock state is no longer a hidden confounder.
- The snapshot parser still depends on the current `state.env` schema owned by lower-layer codex tooling, so future schema drift would need a follow-on owner.
