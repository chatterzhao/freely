# Verification: absorbed-merged-lane-routing-followthrough-governance

- issue_id: `I-20260421-1330-A`
- issue_path: `docs/epics/workspace-routing-foundation/absorbed-merged-lane-routing-followthrough-governance/issues/absorbed-merged-lane-routing-followthrough-governance.md`
- verification_date: `2026-04-21`
- verifier: `codex`

## Scope Verdict

- `PASS`: absorbed merged lanes no longer surface as `role=worker` in fleet status once their branch tip has already been absorbed into `develop`.
- `PASS`: progress items bound to absorbed merged lanes remain visible in task-source-scan, but now route to `cleanup` and manager-owned followthrough instead of `verification` execution.
- `PASS`: fresh branches that still point at current `develop` without an absorbed feature tip are not downgraded, so the fix does not erase legitimate worker lanes.
- `PASS`: focused regressions and existing nearby scan/fleet regressions passed on the source lane.
- `PENDING`: canonical `develop` self-host replay still must prove Freely selects a real launchable task, completes it to the current-project success standard, closes the worktree, and continues.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-wt-fleet-status`
2. `bash docs/system/workspace/scripts/tests/test-wt-fleet-status-absorbed-merged-worker-role`
3. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan`
4. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-routes-absorbed-merged-progress-to-cleanup`
5. `bash docs/system/workspace/scripts/tests/test-freely-task-source-scan-python-compat`
6. `python3 -m py_compile docs/system/workspace/scripts/runtime/task-source-scan.py`
7. `./bin/governance-check`

## Implementation Decision Note

- decision: `Treat absorbed merged lanes as cleanup-visible rather than execution-visible at the fleet snapshot and task-source-scan layers, while preserving their discoverability as unfinished followthrough.`
- why_this: `The prior runtime fixes already blocked automatic relaunch of merged worker lanes. The remaining failure was an advisory-surface mismatch: manager patrol still saw the same absorbed lane as a worker in fleet status and as a verification source in task-source-scan. Downgrading those two surfaces closes the drift without introducing a new lifecycle index or hiding unfinished cleanup work.`
- alternatives_considered: `Only change fleet status and leave scan unchanged; only change scan and leave fleet status misleading; add a durable prompt lifecycle index; hide absorbed merged lanes entirely from scan; reopen the larger daemon self-loop owner.`
- boundary_non_goals: `No scan architecture redesign, no live-status redesign, no reduction in Freely autonomy.`
- residual_risk: `Final canonical develop self-host acceptance still must prove that after this downgrade the manager picks a real launchable task and keeps working autonomously.`
