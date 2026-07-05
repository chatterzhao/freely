# Verification: absorbed-merged-lane-routing-followthrough-governance

- issue_id: `I-20260421-1330-A`
- issue_path: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/issues/absorbed-merged-lane-routing-followthrough-governance.md`
- verification_date: `2026-04-21`
- verifier: `codex`

## Scope Verdict

- `PASS`: absorbed merged lanes no longer surface as `role=worker` in fleet status once their branch tip has already been absorbed into `develop`.
- `PASS`: progress items bound to absorbed merged lanes remain visible in task-source-scan, but now route to `cleanup` and manager-owned followthrough instead of `verification` execution.
- `PASS`: fresh branches that still point at current `develop` without an absorbed feature tip are not downgraded, so the fix does not erase legitimate worker lanes.
- `PASS`: manager startup no longer reuses a stale patrol scan after the project `HEAD` changes; it regenerates scan truth before choosing work.
- `PASS`: when cleanup-governance continuity already contains retained merged targets but no launchable worker prompt, runtime now appends an explicit retirement-worker directive in both `resume` and `fresh_with_handoff` prompts, preventing another no-worker continuity loop from masquerading as progress.
- `PASS`: the retirement-worker directive now accepts both `target_paths:` and canonical daemon `cleanup_targets:` queue fields, so the prompt guard matches real manager continuity output instead of only the reduced fixture format.
- `PASS`: focused regressions and existing nearby scan/fleet regressions passed on the source lane.
- `PASS`: delegated cleanup handoff ancestry proof is now explicit. The absorbed feature tip `9b1fd4c5717652309325b6c6d399e14399559a4d` and absorbed test-pre-merge tip `4941df4b3ee47a8b8c01750178222f21141d26bc` are ancestors of both the handoff's develop tip `d0564874860d15530aa6c8fb97656cec771cc88c` and the current local `develop` tip `cc2a01f26443e27b2ded09842bb61452d2f24b73`.
- `PASS`: `git rev-list --left-right --count` reports `0 66` for `feature/absorbed-merged-scan-routing-fix-20260421...develop` and `0 62` for `test-pre-merge-20260421-absorbed-merged-scan-routing-fix...develop`, so neither retained target carries unique unabsorbed behavior that would justify replay.
- `PASS`: both absorbed targets are now `retire-only` with explicit local/remote branch disposition, so replay is no longer lawful or necessary from this owner.
- `PASS`: fresh 2026-04-22 06:10 UTC cleanup-governance recheck preserved the same ancestry proof, branch-count evidence, remote-branch absence, governance gate pass, and cleanup routing outcome from `freely task-source-scan --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-absorbed-cleanup-retirement-handoff --json`, so the retirement-handoff verdict remains current rather than historical.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-wt-fleet-status`
2. `bash docs/system/workspace/scripts/tests/test-wt-fleet-status-absorbed-merged-worker-role`
3. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan`
4. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-routes-absorbed-merged-progress-to-cleanup`
5. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-idle-continuity-advance`
6. `bash docs/system/workspace/scripts/tests/test-freely-manager-prompt-regenerates-scan-after-head-change`
7. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-python-compat`
8. `python3 -m py_compile docs/system/workspace/scripts/runtime/task-source-scan.py`
9. `./bin/governance-check`
10. `bash docs/system/workspace/scripts/tests/test-freely-cleanup-governance-retirement-worker-directive`
11. `git merge-base --is-ancestor 9b1fd4c5717652309325b6c6d399e14399559a4d d0564874860d15530aa6c8fb97656cec771cc88c`
12. `git merge-base --is-ancestor 4941df4b3ee47a8b8c01750178222f21141d26bc d0564874860d15530aa6c8fb97656cec771cc88c`
13. `git merge-base --is-ancestor 9b1fd4c5717652309325b6c6d399e14399559a4d develop`
14. `git merge-base --is-ancestor 4941df4b3ee47a8b8c01750178222f21141d26bc develop`
15. `git rev-list --left-right --count feature/absorbed-merged-scan-routing-fix-20260421...develop`
16. `git rev-list --left-right --count test-pre-merge-20260421-absorbed-merged-scan-routing-fix...develop`
17. `git ls-remote --heads origin feature/absorbed-merged-scan-routing-fix-20260421 test-pre-merge-20260421-absorbed-merged-scan-routing-fix`
18. `git ls-remote --heads github feature/absorbed-merged-scan-routing-fix-20260421 test-pre-merge-20260421-absorbed-merged-scan-routing-fix`
19. `freely task-source-scan --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260421-feature-absorbed-cleanup-retirement-handoff --json`

## Implementation Decision Note

- decision: `Keep the absorbed-merged routing owner narrow and harden manager prompt execution so retire-only cleanup truth must become a retirement worker handoff instead of another no-worker continuity loop.`
- why_this: `Canonical develop self-host replay already had enough truth to classify the retained merged lanes as cleanup-only, but resume/handoff prompts still left the manager free to write another equivalent continuity and wait. Appending a machine-level retirement-worker directive at prompt-build time is the smallest repair that matches the current orchestration contract without inventing a new lifecycle index or bypassing manager judgement.`
- alternatives_considered: `Wait for the model to infer the stronger obligation from existing skills alone; auto-generate worker prompt files in runtime without the manager round; reopen scan/live-status architecture; manually retire the worktrees outside daemon flow.`
- boundary_non_goals: `No scan architecture redesign, no live-status redesign, no direct auto-deletion bypassing the existing manager/worker cleanup contract.`
- residual_risk: `This round proves replay is closed and the retained targets are retire-only, but actual local branch/worktree deletion still belongs to manager/supervisor cleanup execution after review of this canonical writeback.`

## Cleanup Verdict

- disposition: `retire-only`
- target_feature_local_branch: `retained-with-reason`
- target_feature_remote_branch: `retained-with-reason`
- target_premerge_local_branch: `retained-with-reason`
- target_premerge_remote_branch: `retained-with-reason`
- branch_reason: the worker round writes canonical cleanup truth only; delete execution should happen in the ordinary retirement step, and no matching `origin` or `github` branch exists to delete remotely
- unblock_verdict: `manager can now unblock I-20260421-1200-A`
