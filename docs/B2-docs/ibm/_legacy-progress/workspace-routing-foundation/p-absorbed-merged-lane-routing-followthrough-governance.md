# Progress: absorbed-merged-lane-routing-followthrough-governance

- issue_id: `I-20260421-1330-A`
- issue_path: `docs/B2-docs/ibm/absorbed-merged-lane-routing-followthrough-governance/issues/absorbed-merged-lane-routing-followthrough-governance.md`
- title: `Absorbed merged lane routing followthrough governance`
- phase_state: `completed`
- runtime_state: `closed_for_this_batch`
- milestone: `M-20260306-workspace-routing-foundation`
- branch: `feature/absorbed-cleanup-retirement-handoff-20260421`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-absorbed-cleanup-retirement-handoff`
- updated_at: `2026-04-22 06:10 UTC`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Summary

- Canonical `develop` dogfooding showed the merged-worker relaunch guards were no longer the blocker, but manager patrol still consumed absorbed merged lanes as if they were live worker execution capacity.
- The first drift source was `wt-fleet-status`, which kept `LAST_ROLE_HINT=worker` for absorbed merged lanes and therefore kept rendering them as worker workcells in manager prompts.
- The second drift source was `task-source-scan`, which kept routing linked progress owners to `verification` because it only read progress metadata, not the linked branch/worktree absorption state.
- The bounded fix now downgrades those fleet lanes to cleanup visibility and routes absorbed merged progress items to `cleanup` while preserving scan visibility.
- Canonical `develop` dogfooding then exposed a second drift source: manager startup could still reuse a stale patrol scan after `HEAD` changed, so a just-merged owner could remain launchable from old scan truth even after scan/fleet routing was corrected.
- The follow-up fix now anchors each generated patrol scan to the project `HEAD` and forces regeneration when manager startup observes a different `HEAD`, which keeps startup patrol aligned with post-merge canonical truth.
- Canonical `develop` dogfooding then exposed the next bounded seam in the same owner family: manager continuity could already classify the retained merged lanes as `retire-only`, yet `resume` / `fresh_with_handoff` prompts still allowed another no-worker `cleanup_governance` round instead of demanding a concrete `retirement_handoff` worker.
- Runtime prompt construction now appends an explicit retirement-worker directive whenever the latest cleanup-governance continuity contains retained merged targets but no launchable worker prompt, so the next manager round treats another no-worker continuity as failure rather than acceptable steady state.
- The first pass only matched `target_paths:` from the fixture continuity shape; canonical manager continuity actually emits `cleanup_targets:`. The compatibility followthrough now accepts both field names so the retirement-worker directive fires on real daemon output, not just the reduced test fixture.
- Canonical cleanup followthrough revalidated the delegated handoff's develop tip `d0564874860d15530aa6c8fb97656cec771cc88c` and the current local `develop` tip `cc2a01f26443e27b2ded09842bb61452d2f24b73`: both already contain the absorbed feature tip `9b1fd4c5717652309325b6c6d399e14399559a4d` and the absorbed test-pre-merge tip `4941df4b3ee47a8b8c01750178222f21141d26bc`.
- `git rev-list --left-right --count feature/absorbed-merged-scan-routing-fix-20260421...develop` now returns `0 66`, and `git rev-list --left-right --count test-pre-merge-20260421-absorbed-merged-scan-routing-fix...develop` returns `0 62`, so neither retained target carries unique unabsorbed behavior relative to canonical `develop`.
- Both absorbed targets are now explicitly classified as `retire-only`; this owner no longer lawfully points manager back to guarded replay or canonical self-host execution.
- Fresh 2026-04-22 06:10 UTC recheck kept the same verdict: all four `git merge-base --is-ancestor` proofs still pass, `git rev-list --left-right --count` remains `0 66` and `0 62`, `git ls-remote --heads origin/github` still finds no matching remote branches, `./bin/governance-check` still passes, and a fresh `freely task-source-scan --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-absorbed-cleanup-retirement-handoff --json` patrol still keeps this owner in cleanup-governance / retirement_handoff followthrough rather than replay; manager can unblock `I-20260421-1200-A` once ordinary retirement cleanup executes.

## Cleanup Followthrough

- disposition: `retire-only`
- cleanup_gate: `manager-review-ready`
- target_feature_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-absorbed-merged-scan-routing-fix`
- target_feature_branch: `feature/absorbed-merged-scan-routing-fix-20260421`
- target_feature_local_branch_disposition: `retained-with-reason`
- target_feature_local_branch_reason: implementation commits are already absorbed by `develop`, but this worker round only writes canonical cleanup truth; branch/worktree deletion should happen in the normal manager/supervisor retirement step after review
- target_feature_remote_branch_disposition: `retained-with-reason`
- target_feature_remote_branch_reason: no matching `origin` or `github` remote branch exists, so there is nothing to delete remotely
- target_premerge_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-test-pre-merge-absorbed-merged-scan-routing-fix`
- target_premerge_branch: `test-pre-merge-20260421-absorbed-merged-scan-routing-fix`
- target_premerge_local_branch_disposition: `retained-with-reason`
- target_premerge_local_branch_reason: the batch is already absorbed and clean, but worker scope in this round is limited to canonical handoff writeback rather than deleting protected-family validation branches directly
- target_premerge_remote_branch_disposition: `retained-with-reason`
- target_premerge_remote_branch_reason: no matching `origin` or `github` remote branch exists, so there is nothing to delete remotely
- revisit_trigger: reopen only if a fresh ancestry audit later shows either target has unique non-`develop` behavior, or if manager retirement review finds a concrete blocker to deleting the now-absorbed local branches/worktrees

## Verification Evidence

1. `bash docs/system/workspace/scripts/tests/test-wt-fleet-status`
2. `bash docs/system/workspace/scripts/tests/test-wt-fleet-status-absorbed-merged-worker-role`
3. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan`
4. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-routes-absorbed-merged-progress-to-cleanup`
5. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`
6. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-head-change`
7. `./bin/governance-check`
8. `docs/B2-docs/ibm/absorbed-merged-lane-routing-followthrough-governance/code-reviews/20260421-absorbed-merged-lane-routing-followthrough-verification.md`
9. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-governance-retirement-worker-directive`
10. `git merge-base --is-ancestor 9b1fd4c5717652309325b6c6d399e14399559a4d d0564874860d15530aa6c8fb97656cec771cc88c`
11. `git merge-base --is-ancestor 4941df4b3ee47a8b8c01750178222f21141d26bc d0564874860d15530aa6c8fb97656cec771cc88c`
12. `git merge-base --is-ancestor 9b1fd4c5717652309325b6c6d399e14399559a4d develop`
13. `git merge-base --is-ancestor 4941df4b3ee47a8b8c01750178222f21141d26bc develop`
14. `git rev-list --left-right --count feature/absorbed-merged-scan-routing-fix-20260421...develop`
15. `git rev-list --left-right --count test-pre-merge-20260421-absorbed-merged-scan-routing-fix...develop`
16. `git ls-remote --heads origin feature/absorbed-merged-scan-routing-fix-20260421 test-pre-merge-20260421-absorbed-merged-scan-routing-fix`
17. `git ls-remote --heads github feature/absorbed-merged-scan-routing-fix-20260421 test-pre-merge-20260421-absorbed-merged-scan-routing-fix`

## Next Action

1. Keep this owner closed as cleanup-governance / retirement_handoff truth rather than reopening canonical replay from this worktree.
2. Manager can now review the linked ancestry proof, then retire `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-absorbed-merged-scan-routing-fix` and `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-test-pre-merge-absorbed-merged-scan-routing-fix`.
3. After those branches/worktrees are retired, `I-20260421-1200-A` no longer needs to wait on this absorbed lane.
