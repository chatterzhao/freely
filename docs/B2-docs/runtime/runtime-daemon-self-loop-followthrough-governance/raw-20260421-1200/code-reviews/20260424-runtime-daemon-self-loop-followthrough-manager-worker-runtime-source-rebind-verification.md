# Verification: runtime-daemon-self-loop-followthrough-governance manager-owned worker runtime source rebind

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-24`
- verifier: `codex`
- source_branch: `feature/manager-worker-runtime-source-rebind-20260424`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-manager-worker-runtime-source-rebind`

## Scope Verdict

- `FAIL`: canonical `develop` continuity-first replay still could not close the retained cleanup lane after the worker-exit-contract repair because that active worker was still being supervised by its own stale worktree runtime instead of the current canonical manager runtime.
- `PASS`: the observed retained lane had already emitted lawful `EXIT_KIND="worker_done"` truth, so the remaining blocker was control-plane ownership. New closeout logic merged into `develop` could not govern that lane while relaunch/reentry kept using the target worktree's older runtime script.
- `PASS`: manager-owned worker launches now bind to the manager/source runtime bin when source and target projects differ, and active-worker reconciliation now rebinding-stops stale worker control planes before relaunching them under the manager/source runtime.
- `PASS`: this is intentionally narrow. It does not widen task selection, weaken continuity-first behavior, or bypass the existing active-worker checks; it only ensures the already-selected retained lane is supervised by the authoritative runtime implementation.
- `PENDING`: guarded premerge and canonical `develop` replay still need to prove the retained lane closes from its existing completion contract, merges/retires lawfully, and Freely then resumes scan-selected backlog.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-start-workcell-supervisor-uses-source-runtime-bin`
2. `bash docs/system/workspace/scripts/tests/test-freely-worker-launch-rebinds-stale-active-runtime-control-plane`
3. `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
4. `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`
5. `bash -n docs/system/workspace/scripts/runtime/freely`

## Implementation Decision Note

- decision: `Keep manager-owned worker supervision on the manager/source runtime and force a controlled handoff when an already-active worker is still attached to stale target-runtime code.`
- why_this: `The autonomy loop was no longer blocked by task choice or worker completion truth. It was blocked because retained workers could keep running under older worktree-local runtime code that never received the newer closeout fixes merged into canonical develop.`
- alternatives_considered: `Restart the full daemon manually every time a retained worktree lags; copy runtime scripts into active worktrees opportunistically; weaken continuity and mint a fresh replacement worker lane.`
- boundary_non_goals: `No scan-json policy change, no runtime-owned artifact contract redesign, no worker prompt format change, and no claim that end-to-end daemon autonomy is complete before canonical replay proves closeout and next-task advancement.`
- residual_risk: `Canonical replay may still expose a later merge, retirement, or next-task selection seam after the stale control plane is rebound, but the retained worker should no longer stay pinned to obsolete runtime logic.`
