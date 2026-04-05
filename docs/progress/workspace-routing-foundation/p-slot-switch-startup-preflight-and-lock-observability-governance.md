# Progress: slot-switch-startup-preflight-and-lock-observability-governance

- issue_id: `I-20260404-2148-A`
- issue_path: `docs/epics/workspace-routing-foundation/slot-switch-startup-preflight-and-lock-observability-governance/issues/slot-switch-startup-preflight-and-lock-observability-governance.md`
- title: `Slot-switch startup preflight and lock observability governance`
- phase_state: `in_dev`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/slot-switch-startup-preflight-governance-20260404-2138`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260404-2138-feature-slot-switch-startup-preflight-governance`
- updated_at: `2026-04-04`
- closure_status: `in_progress`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- The owner is now materialized as a dedicated startup-governance issue instead of remaining an unresolved candidate mixed with blocked-intake supervision.
- Current root failure evidence is still `auth_failure`, not a current lock, but the stale shared lock blocker is documented and remains the implementation trigger for this issue.
- Runtime implementation is next: startup preflight plus structured lock truth on doctor/status surfaces.

## Current Batch Risks

1. The lock snapshot taxonomy could drift if startup and observability each invent slightly different meanings for `stale` and `ambiguous`.
2. Existing lower-layer helpers in `tool-launchers.sh` and `ai-cli` could diverge from the new `freely` preflight if the shared semantics are not kept narrow.

## Next Action

1. Implement shared slot-switch lock snapshot helpers in `runtime/freely`.
2. Add focused tests for stale cleanup, active timeout, and structured status/doctor visibility.
3. Write the implementation decision note after the final helper insertion points are fixed.
