# Progress: runtime-startup-self-healing-governance

- issue_id: `I-20260419-1630-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/issues/runtime-startup-self-healing-governance.md`
- title: `Runtime startup self-healing governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-startup-self-healing-boundary-20260419`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260419-feature-runtime-startup-self-healing-boundary`
- updated_at: `2026-04-19`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Protected-root replay exposed stale startup machine state before manager launch: `running/up/starting` truth stayed on disk after owned runtime processes were already gone.
- This owner freezes a narrow line: startup repairs only script-provable stale state; manager recovery still owns semantic continuation after startup truth is canonical.
- The current implementation adds pre-start/status self-heal hooks plus launch-state writeback hardening.
- Focused regressions, protected-root replay, and governance-gate closure are complete; the remaining work is merge/push/retirement.

## Success Criteria

1. Protected-root stale startup truth is canonicalized before startup/status consumers rely on it.
2. Attach/reuse, daemon cold-start, and restart semantics remain intact.
3. Verification evidence is written back, then this lane merges to `develop`, pushes, and retires.

## Current Evidence

1. Real replay on `2026-04-19` recorded stale `supervisor.pid` and `interruption-dispatch.pid` under `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/` while no owned runtime processes remained.
2. The same protected-root state still showed `DESIRED_RUNTIME_STATE="running"`, `LAST_SUPERVISOR_STATE="up"`, and `LAST_EXIT_REASON="starting"`.
3. Continuity and prompt artifacts still referenced missing worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260413-feature-runtime-manager-startup-blocker-rootcause`.
4. Protected-root replay at `2026-04-20 00:40-00:42 PDT` self-healed both the older stale startup state and the new failed startup attempt back to `startup_self_heal_no_runtime`, while surfacing `manager_continuity_gap_state: active` instead of fake runtime liveness.
5. `./bin/governance-check` now passes after `governance-check` learned to validate `unparseable_subject_ancestry` receipt-gap entries even after their target `test-pre-merge-*` branch has been lawfully absorbed and deleted.

## Next Action

1. Merge to `develop`, push, and retire the dedicated worktree/branch.
