# Verification: runtime-daemon-self-loop-followthrough-governance worker materialization and summary followthrough

- issue_id: `I-20260421-1200-A`
- date: `2026-04-23`
- scope: `Keep daemon patrol pipe-safe, let manager materialize governed missing worker lanes from prompt metadata, and prevent authoritative edit ownership from being auto-retired as merged cleanup.`

## Findings

- `FAIL`: canonical `develop` replay had already narrowed to the retained dirty cleanup lane, but `worktree_summary_for_project()` could still emit `printf: write error: Broken pipe`, which is enough to degrade patrol/live-status consumers while the daemon is trying to continue.
- `FAIL`: manager could choose a launchable worker prompt from continuity/scan and still reject it because the sibling worktree did not exist yet, even though the prompt already carried lawful `Worktree:` and `Branch:` headers inside the governed `*-worktrees` root.
- `FAIL`: once a worker lane existed and its branch tip was merged, runtime could still misclassify it as retire-ready merged cleanup despite the latest authoritative continuity still granting active `edit` ownership to that lane.
- `PASS`: the summary path now iterates worktree porcelain directly and writes the final `total|dirty` output through a pipe-tolerant block, so a closed downstream consumer no longer turns into patrol failure.
- `PASS`: exit-contract validation and manager worker launch now treat governed missing sibling worktrees as materializable, create them before launch, and refresh discovery so scan-selected prompts can become real worker workcells.
- `PASS`: merged-tip absorbed/retire-ready classification now refuses reclamation whenever the latest authoritative continuity still carries a non-cleanup prompt for that lane, preserving real selected-task ownership.

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-worktree-summary-multi-worktree`
- `bash docs/system/workspace/scripts/tests/test-freely-worktree-summary-tolerates-closed-pipe`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-allows-materializable-missing-worktree`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-materializes-missing-worktree`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-keeps-fresh-materialized-worker-with-authoritative-edit-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-materialized-cleanup-worker-without-continuity-prompt`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-worktree-summary-multi-worktree`
- `./bin/test-lane premerge-integration -- bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-materializes-missing-worktree`
- `./bin/test-lane premerge-integration -- ./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260423-test-pre-merge-worker-materialization --issue docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- `./bin/test-lane premerge-integration -- ./bin/governance-check`

## Status

- `PASS`: focused feature-lane regressions prove manager can now convert continuity-selected worker prompts into actual governed worktrees without tripping the old broken-pipe or retire-ready misclassification seams.
- `PASS`: protected `test-pre-merge-20260423-worker-materialization` replay reran the bounded summary/materialization checks plus owner gates, so develop-bound adequacy now has a fresh staged owner review artifact for this repair family.
- `PENDING`: protected premerge plus canonical `develop` daemon replay still must show the retained cleanup lane closes and the next scan-selected task begins automatically.

## Implementation Decision Note

- decision: `Keep the repair inside the existing daemon self-loop followthrough owner instead of reopening a broader worker-launch or cleanup governance issue.`
- why_this: `The new failures were discovered only after the daemon had already selected the retained cleanup path; both the broken-pipe summary seam and missing-worktree materialization seam directly block the same end-to-end self-loop acceptance surface.`
- alternatives_considered: `Treat broken-pipe summary as a separate status-only bug; require pre-existing worktrees for every worker prompt; allow merged-tip edit lanes to be reclaimed as cleanup if their branch is already merged.`
- boundary_non_goals: `No redesign of scan ranking, no new worktree topology, no broad cleanup-governance rewrite, and no claim that canonical develop success-standard acceptance is complete before protected replay proves it.`
- residual_risk: `Canonical replay may still expose a narrower followthrough seam after these launchability repairs land, but manager should now at least be able to materialize selected work lanes and keep authoritative edit ownership intact instead of stalling before execution.`
