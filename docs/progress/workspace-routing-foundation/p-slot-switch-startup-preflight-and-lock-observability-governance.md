# Progress: slot-switch-startup-preflight-and-lock-observability-governance

- issue_id: `I-20260404-2148-A`
- issue_path: `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/issues/slot-switch-startup-preflight-and-lock-observability-governance.md`
- title: `Slot-switch startup preflight and lock observability governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/slot-switch-startup-preflight-governance-20260404-2138`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260404-2138-feature-slot-switch-startup-preflight-governance`
- updated_at: `2026-04-04`
- closure_status: `ready_for_merge`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- The owner is now materialized as a dedicated startup-governance issue instead of remaining an unresolved candidate mixed with blocked-intake supervision.
- Root evidence still says the current startup failure is `auth_failure`, not a live shared slot-switch lock, so this owner stayed narrow instead of reopening supervision or intake continuity.
- `docs/system/workspace/scripts/runtime/freely` now snapshots the shared lock into `idle | active | stale | ambiguous`, runs startup preflight before supervisor bootstrap, auto-cleans only `stale`, and surfaces the same structured lock truth through `doctor`, `baseline-status`, and `live-status`.
- Focused regressions and `./bin/governance-check` passed on this feature lane, so the batch is ready for guarded merge into `develop`.

## Verification Snapshot

- Passed in this worktree:
  - `bash -n docs/system/workspace/scripts/runtime/freely`
  - `bash docs/system/workspace/scripts/tests/test-freely-start-cleans-stale-slot-switch-lock`
  - `bash docs/system/workspace/scripts/tests/test-freely-start-times-out-on-active-slot-switch-lock`
  - `bash docs/system/workspace/scripts/tests/test-freely-slot-switch-lock-status-surface`
  - `bash docs/system/workspace/scripts/tests/test-freely-status-family`
  - `./bin/governance-check`

## Next Action

1. Keep this owner in `in_verification` and merge the lane into `develop`.
2. After develop absorption, confirm canonical root status/doctor surfaces still emit the same `current_slot_switch_lock_*` fields.
3. If startup remains broken due to `auth_failure` afterward, route that as separate follow-on governance instead of widening `2148`.
