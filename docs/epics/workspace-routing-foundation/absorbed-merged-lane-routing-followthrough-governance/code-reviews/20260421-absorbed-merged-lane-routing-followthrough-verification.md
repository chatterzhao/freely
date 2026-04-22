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
- `PENDING`: canonical `develop` self-host replay still must prove Freely selects a real launchable task, completes it to the current-project success standard, closes the worktree, and continues.

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

## Implementation Decision Note

- decision: `Keep the absorbed-merged routing owner narrow and harden manager prompt execution so retire-only cleanup truth must become a retirement worker handoff instead of another no-worker continuity loop.`
- why_this: `Canonical develop self-host replay already had enough truth to classify the retained merged lanes as cleanup-only, but resume/handoff prompts still left the manager free to write another equivalent continuity and wait. Appending a machine-level retirement-worker directive at prompt-build time is the smallest repair that matches the current orchestration contract without inventing a new lifecycle index or bypassing manager judgement.`
- alternatives_considered: `Wait for the model to infer the stronger obligation from existing skills alone; auto-generate worker prompt files in runtime without the manager round; reopen scan/live-status architecture; manually retire the worktrees outside daemon flow.`
- boundary_non_goals: `No scan architecture redesign, no live-status redesign, no direct auto-deletion bypassing the existing manager/worker cleanup contract.`
- residual_risk: `Canonical develop self-host acceptance still must prove the next manager round actually emits and consumes the cleanup worker, closes the retained merged worktrees, and then advances to another task.`
