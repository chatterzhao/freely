# Issue: absorbed-merged-lane-routing-followthrough-governance

- issue_id: `I-20260421-1330-A`
- title: `Absorbed merged lane routing followthrough governance`
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `absorbed-merged-lane-routing-followthrough-governance`
- issue-name: `absorbed-merged-lane-routing-followthrough-governance`
- priority: `P0`
- source_candidate: `docs/B1-docs/raw-20260421/candidates.md#c-20260421-1330-a`
- source_brainstorm: `docs/B1-docs/raw-20260421/brainstorms.md`
- reopen_of_issue: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- reopen_reason: `canonical develop self-host replay proved absorbed merged blocker lanes were no longer auto-recovered, but scan/fleet patrol still routed them as if they were launchable worker execution targets`
- execution_base: `develop`
- integration_target: `develop`
- pre_tests_path: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/pre-tests.md`
- tasks_path: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/tasks.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-absorbed-merged-lane-routing-followthrough-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/code-reviews`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- created_at: `2026-04-21`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

The previous runtime repairs already blocked automatic relaunch of merged worker lanes. The remaining failure was subtler: manager patrol still looked at absorbed merged lanes and treated them like current execution capacity.

Two bounded surfaces caused that drift:

1. `wt-fleet-status` preserved `LAST_ROLE_HINT=worker` even when the branch tip was already absorbed into `develop`.
2. `task-source-scan` kept routing linked progress items back to `verification` because it did not consult the linked branch/worktree absorption state.

This owner exists to downgrade those absorbed lanes to cleanup-followthrough visibility without hiding them from scan, so Freely keeps autonomy while choosing real launchable tasks next.

## Scope

1. Downgrade absorbed merged lanes in fleet status from `worker` to cleanup-like role visibility.
2. Route absorbed merged progress items to `cleanup` instead of `verification`, while keeping them visible as unfinished followthrough.
3. Add focused regressions for both downgraded surfaces plus nearby scan/fleet coverage.
4. Reconfirm the guarded feature -> test-pre-merge -> develop chain is already absorbed by canonical `develop`, including the develop tip referenced by delegated cleanup handoff.
5. Record explicit retirement-handoff disposition for the absorbed feature/test-pre-merge pair so they stop masquerading as replay-ready worker lanes.
6. Keep cleanup-governance continuity on the bounded `retirement_handoff` path rather than reopening canonical self-host replay from this owner.

## Non-Goals

1. Do not redesign scan, live-status, or manager continuity architecture.
2. Do not add a durable prompt lifecycle index.
3. Do not weaken Freely's ability to self-select work from scan.
4. Do not reopen the broader daemon self-loop implementation owner.

## Acceptance

1. Absorbed merged lanes no longer render as `worker` in fleet status.
2. Task-source scan routes absorbed merged progress owners to cleanup-style followthrough instead of verification execution.
3. Focused regressions and existing nearby scan/fleet regressions pass.
4. Linked git ancestry proof confirms the absorbed feature tip and absorbed test-pre-merge tip are already ancestors of the delegated handoff's develop tip and the current canonical `develop`.
5. The absorbed feature/test-pre-merge pair now has explicit `retire-only` disposition plus local/remote branch disposition, so this owner no longer instructs replay.

## Verification

- `bash docs/system/workspace/scripts/tests/test-wt-fleet-status`
- `bash docs/system/workspace/scripts/tests/test-wt-fleet-status-absorbed-merged-worker-role`
- `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan`
- `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-routes-absorbed-merged-progress-to-cleanup`
- `bash docs/system/workspace/scripts/tests/test-freely-cleanup-governance-retirement-worker-directive`
- `git merge-base --is-ancestor 9b1fd4c5717652309325b6c6d399e14399559a4d d0564874860d15530aa6c8fb97656cec771cc88c`
- `git merge-base --is-ancestor 4941df4b3ee47a8b8c01750178222f21141d26bc d0564874860d15530aa6c8fb97656cec771cc88c`
- `git merge-base --is-ancestor 9b1fd4c5717652309325b6c6d399e14399559a4d develop`
- `git merge-base --is-ancestor 4941df4b3ee47a8b8c01750178222f21141d26bc develop`
- `git rev-list --left-right --count feature/absorbed-merged-scan-routing-fix-20260421...develop`
- `git rev-list --left-right --count test-pre-merge-20260421-absorbed-merged-scan-routing-fix...develop`
- `git ls-remote --heads origin feature/absorbed-merged-scan-routing-fix-20260421 test-pre-merge-20260421-absorbed-merged-scan-routing-fix`
- `git ls-remote --heads github feature/absorbed-merged-scan-routing-fix-20260421 test-pre-merge-20260421-absorbed-merged-scan-routing-fix`
- `./bin/governance-check`

## Completion

- `docs/B1-docs/raw-20260421/brainstorms.md`
- `docs/B1-docs/raw-20260421/candidates.md`
- `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/issues/absorbed-merged-lane-routing-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/pre-tests.md`
- `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/tasks.md`
- `docs/progress/workspace-routing-foundation/p-absorbed-merged-lane-routing-followthrough-governance.md`
- `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/code-reviews/20260421-absorbed-merged-lane-routing-followthrough-verification.md`
- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/task-source-scan.py`
- `docs/system/workspace/scripts/worktree/wt-fleet-status`
- `docs/system/workspace/scripts/tests/test-wt-fleet-status-absorbed-merged-worker-role`
- `docs/system/workspace/scripts/tests/test-freely-task-source-scan-routes-absorbed-merged-progress-to-cleanup`
- `docs/system/workspace/scripts/tests/test-freely-cleanup-governance-retirement-worker-directive`

## Cleanup Followthrough

- disposition: `retire-only`
- cleanup_gate: `manager-review-ready`
- target_feature_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-absorbed-merged-scan-routing-fix`
- target_feature_branch: `feature/absorbed-merged-scan-routing-fix-20260421`
- target_feature_local_branch_disposition: `retained-with-reason`
- target_feature_local_branch_reason: deletion is deferred to the ordinary manager/supervisor retirement step after canonical cleanup review
- target_feature_remote_branch_disposition: `retained-with-reason`
- target_feature_remote_branch_reason: no matching `origin` or `github` remote branch exists to delete
- target_premerge_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-test-pre-merge-absorbed-merged-scan-routing-fix`
- target_premerge_branch: `test-pre-merge-20260421-absorbed-merged-scan-routing-fix`
- target_premerge_local_branch_disposition: `retained-with-reason`
- target_premerge_local_branch_reason: deletion is deferred to the ordinary manager/supervisor retirement step after canonical cleanup review
- target_premerge_remote_branch_disposition: `retained-with-reason`
- target_premerge_remote_branch_reason: no matching `origin` or `github` remote branch exists to delete
- revisit_trigger: reopen only if a fresh ancestry audit finds unique non-`develop` behavior or if manager retirement review discovers a concrete deletion blocker

## Next

- 当前 issue 的实现与 develop absorption 已完成。
- 当前只剩 cleanup-governance / retirement_handoff followthrough：manager review 当前 round 的 ancestry proof、retire-only disposition 与 branch disposition 后，即可把 absorbed feature/test-pre-merge pair 从 active fleet 中退休。
- 若未来再次发现 absorbed merged lanes 被 scan/fleet 重新当成 edit-ready execution capacity，应以新的 bounded follow-on reopen，而不是回放本 issue 的 canonical replay。
- Fresh 2026-04-22 06:10 UTC cleanup-governance recheck kept the same verdict: delegated-hand-off develop tip `d0564874860d15530aa6c8fb97656cec771cc88c` and current local `develop` still absorb both target tips, both cleanup targets remain `retire-only`, no matching remote branches exist, a fresh task-source-scan patrol still keeps this owner on cleanup-governance / retirement_handoff followthrough rather than replay, and manager may now unblock `I-20260421-1200-A` after ordinary retirement cleanup.
