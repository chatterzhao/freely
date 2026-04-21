# Progress: absorbed-merged-lane-routing-followthrough-governance

- issue_id: `I-20260421-1330-A`
- issue_path: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/issues/absorbed-merged-lane-routing-followthrough-governance.md`
- title: `Absorbed merged lane routing followthrough governance`
- phase_state: `in_verification`
- runtime_state: `stopped`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/absorbed-merged-scan-routing-fix-20260421`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-absorbed-merged-scan-routing-fix`
- updated_at: `2026-04-21 14:07 PDT`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Canonical `develop` dogfooding showed the merged-worker relaunch guards were no longer the blocker, but manager patrol still consumed absorbed merged lanes as if they were live worker execution capacity.
- The first drift source was `wt-fleet-status`, which kept `LAST_ROLE_HINT=worker` for absorbed merged lanes and therefore kept rendering them as worker workcells in manager prompts.
- The second drift source was `task-source-scan`, which kept routing linked progress owners to `verification` because it only read progress metadata, not the linked branch/worktree absorption state.
- The bounded fix now downgrades those fleet lanes to cleanup visibility and routes absorbed merged progress items to `cleanup` while preserving scan visibility.
- Canonical `develop` dogfooding then exposed a second drift source: manager startup could still reuse a stale patrol scan after `HEAD` changed, so a just-merged owner could remain launchable from old scan truth even after scan/fleet routing was corrected.
- The follow-up fix now anchors each generated patrol scan to the project `HEAD` and forces regeneration when manager startup observes a different `HEAD`, which keeps startup patrol aligned with post-merge canonical truth.
- Focused regressions and nearby scan/fleet/prompt tests now pass; remaining work is guarded replay into `develop`, canonical self-host acceptance, and temporary worktree retirement.

## Verification Evidence

1. `bash docs/system/workspace/scripts/tests/test-wt-fleet-status`
2. `bash docs/system/workspace/scripts/tests/test-wt-fleet-status-absorbed-merged-worker-role`
3. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan`
4. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-routes-absorbed-merged-progress-to-cleanup`
5. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`
6. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-head-change`
7. `./bin/governance-check`
8. `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/code-reviews/20260421-absorbed-merged-lane-routing-followthrough-verification.md`

## Next Action

1. Replay `feature/absorbed-merged-scan-routing-fix-20260421 -> test-pre-merge-20260421-absorbed-merged-scan-routing-fix -> develop`.
2. On canonical `develop`, rerun `./bin/freely daemon start` until Freely completes one real task to the current-project success standard and begins the next.
3. Retire the temporary feature and test-pre-merge worktrees once canonical develop absorbs the fix.
