# Progress: runtime-startup-self-healing-governance

- issue_id: `I-20260419-1630-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-startup-self-healing-governance/issues/runtime-startup-self-healing-governance.md`
- title: `Runtime startup self-healing governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/runtime-manager-startup-blocker-rootcause-20260419`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260419-feature-runtime-manager-startup-blocker-rootcause`
- updated_at: `2026-04-20`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Protected-root replay exposed two adjacent startup seams: stale machine-owned state before manager launch, and prompt-build-stage supervisor loss that later got mislabeled as `startup_self_heal_no_runtime`.
- This owner keeps the same narrow line: startup repairs only script-provable stale state, but now also records launch-in-flight truth and preserves retryable prompt-build failure under a live supervisor.
- The current implementation adds launch-state writeback hardening plus a prompt-build failure retry path that is tool-agnostic and compatible with short-lived non-interactive CLI tools.
- A follow-on continuation on `2026-04-20` fixes one more narrow ownership seam: `live-status` must not clear a live daemon when the recorded project root and inspected project root are the same directory but spelled with different casing/path forms.
- A fresh-session reentry on `2026-04-20` consumed the `context_compacted` handoff and confirmed this lane remains a verification continuation, so the first closeout duty is still to keep the verification artifact current instead of reopening implementation scope.
- The delegated continuation `20260419-232124-blocker-docs-project-intent-md-h` was re-read during the fresh-session reentry; after no higher-priority blocker surfaced from milestones, progress, review/test, session evidence, GitHub-like repo evidence, or `PROJECT_INTENT`, this worktree absorbs the requested one-line marker as a sidecar continuity action without changing the startup self-heal acceptance boundary.
- The same dirty tree also carries several runtime hardening tests outside this owner's acceptance surface: `test-freely-session-rotation`, `test-freely-delegated-continuation-ids-empty-success`, `test-freely-delegated-continuation-prompt-contract`, `test-freely-interruption-dispatcher-ready-loop-tolerates-empty-probe-failure`, and `test-freely-post-cycle-helper-failure-does-not-kill-supervisor` align with delegated-continuation/session-rotation/readiness-resilience contracts rather than startup self-heal.
- The same fresh-session rerun also kept the continuity-specific guards green: `test-freely-manager-launch-state-refresh-persists-stale-continuity-rewrite` and `test-freely-stale-manager-continuity-filter` still pass after the path-equivalence followthrough, so this lane's continuity rewrite/filter contract remains intact.
- Focused regressions are green in the current worker worktree; the remaining work is to refresh verification evidence and finish the guarded merge chain for this continuation.

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
7. `bash docs/system/workspace/scripts/tests/test-freely-live-status-keeps-daemon-runtime-across-case-variant-project-path` now passes on `2026-04-20`, proving pid/supervisor ownership checks preserve a live daemon when `os.path.samefile()` shows the recorded project root and inspected project root are the same directory.
8. `bash docs/system/workspace/scripts/tests/test-freely-live-status-startup-self-heals-stale-runtime-state`, `bash docs/system/workspace/scripts/tests/test-freely-live-status`, `bash -n docs/system/workspace/scripts/runtime/freely`, `git diff --check`, and `./bin/governance-check` all pass in `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260419-feature-runtime-manager-startup-blocker-rootcause`.
9. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-persists-stale-continuity-rewrite` and `bash docs/system/workspace/scripts/tests/test-freely-stale-manager-continuity-filter` also pass on `2026-04-20`, so the continuity refresh/filter edge covered by this owner remains stable in the fresh session.
10. `docs/PROJECT_INTENT.md` now ends with `<!-- runtime-lifecycle-validation -->` so the delegated continuation has a durable repository marker while this worker lane stays on the same verification closeout path.

## Next Action

1. Preserve the verification-first route: keep the refreshed case-variant path evidence in the verification artifact, then finish the guarded `feature -> test-pre-merge -> develop` merge chain for the current continuation and retire the dedicated worktree/branch.
2. Treat the `docs/PROJECT_INTENT.md` marker as absorbed delegated continuity evidence only; do not let it widen the startup self-heal acceptance surface or replace the remaining guarded promote duties.
3. Before guarded promote, split or reroute the cross-owner dirty tests in this worktree unless a later bounded review proves they are required by this owner's acceptance surface: `test-freely-session-rotation`, `test-freely-delegated-continuation-ids-empty-success`, `test-freely-delegated-continuation-prompt-contract`, `test-freely-interruption-dispatcher-ready-loop-tolerates-empty-probe-failure`, and `test-freely-post-cycle-helper-failure-does-not-kill-supervisor`.
