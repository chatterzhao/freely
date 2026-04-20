# Progress: runtime-startup-self-healing-governance

- issue_id: `I-20260419-1630-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/issues/runtime-startup-self-healing-governance.md`
- title: `Runtime startup self-healing governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-startup-self-healing-followthrough-20260419`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260419-feature-runtime-startup-self-healing-followthrough`
- updated_at: `2026-04-19`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Protected-root replay exposed two adjacent startup seams: stale machine-owned state before manager launch, and prompt-build-stage supervisor loss that later got mislabeled as `startup_self_heal_no_runtime`.
- This owner keeps the same narrow line: startup repairs only script-provable stale state, but now also records launch-in-flight truth and preserves retryable prompt-build failure under a live supervisor.
- The current implementation adds launch-state writeback hardening plus a prompt-build failure retry path that is tool-agnostic and compatible with short-lived non-interactive CLI tools.
- Focused regressions and protected-root replay are complete; the remaining work is guarded merge chain completion and retirement.

## Success Criteria

1. Protected-root stale startup truth is canonicalized before startup/status consumers rely on it.
2. Attach/reuse, daemon cold-start, and restart semantics remain intact.
3. Verification evidence is written back, then this lane merges to `develop`, pushes, and retires.

## Current Evidence

1. Real replay on `2026-04-19` recorded stale `supervisor.pid` and `interruption-dispatch.pid` under `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/` while no owned runtime processes remained.
2. The same protected-root state still showed `DESIRED_RUNTIME_STATE="running"`, `LAST_SUPERVISOR_STATE="up"`, and `LAST_EXIT_REASON="starting"`.
3. Continuity and prompt artifacts still referenced missing worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260413-feature-runtime-manager-startup-blocker-rootcause`.
4. Feature-lane replay on `2026-04-19 20:29 PDT` no longer collapsed to `startup_self_heal_no_runtime`; it stopped in explicit governance state `manager_worker_launch_verification_blocked`, proving the startup self-heal path was no longer misclassifying the lane.
5. Protected-root replay on `2026-04-19 20:57-20:58 PDT` stayed live after prompt build and reached `desired_runtime_state: running`, `last_supervisor_state: up`, `last_ai_state: up` under `tool=codex`, instead of dying at `L020 prompt_build_begin` and self-healing to `startup_self_heal_no_runtime`.
6. The new regressions `test-monitor-ai-cli-pid`, `test-freely-live-status-startup-self-heals-stale-launch-in-flight-state`, and `test-freely-prompt-build-failure-keeps-supervisor-alive` all pass alongside the existing startup-self-heal and supervisor-event tests.

## Next Action

1. Finish the guarded `feature -> test-pre-merge -> develop` merge chain, then retire the dedicated worktree/branch.
