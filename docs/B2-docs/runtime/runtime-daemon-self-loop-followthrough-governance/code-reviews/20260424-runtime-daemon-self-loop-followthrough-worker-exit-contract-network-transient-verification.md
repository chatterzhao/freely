# Verification: runtime-daemon-self-loop-followthrough-governance worker exit contract network transient precedence

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/epics/workspace-routing-foundation/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-24`
- verifier: `codex`
- source_branch: `feature/worker-exit-contract-network-transient-precedence-20260424`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-worker-exit-contract-network-transient-precedence`

## Scope Verdict

- `FAIL`: canonical `develop` continuity-first replay still could not close the retained cleanup-followthrough lane after queued-owner self-block was removed, because the worker had already written a valid `worker_done` contract while runtime still classified the same AI cycle as `execution_network_transient` and relaunched it.
- `PASS`: the defect was not in scan-json selection or manager continuity. Root manager truth still waited on the retained lane first; the loop persisted because worker exit-contract consumption only ran on `ai_exit_rc_0`.
- `PASS`: runtime now consumes a valid worker exit contract before bounded network relaunch when the exit reason is `execution_network_transient`, `execution_network_persistent`, or `proxy_config_invalid`, while leaving missing/invalid contracts on the existing network-recovery path.
- `PASS`: this repair stays narrow. It does not broaden manager authority, does not relax invalid-contract repair, and does not turn network failures into fake completion unless a valid worker contract is already on disk.
- `PENDING`: guarded premerge and canonical `develop` replay still must prove the retained lane now stops at lawful worker completion, proceeds through manager review / protected promotion / retirement, and then advances to the next scan-selected task.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-stops-ai`
2. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-done-overrides-network-transient`
3. `bash docs/system/workspace/scripts/tests/test-freely-worker-exit-contract-invalid-does-not-override-network-transient`
4. `bash -n docs/system/workspace/scripts/runtime/freely`

## Implementation Decision Note

- decision: `Let valid worker exit contracts override reconnect-classified runtime failure only after the contract file exists and validates.`
- why_this: `The retained worker lane had already emitted lawful machine-readable completion, so continuing to prioritize reconnect recovery over that contract turned a bounded transient into an infinite self-loop.`
- alternatives_considered: `Consume all worker contracts regardless of exit reason; treat reconnect-classified exits as invalid-contract repair; suppress network recovery whenever any contract file exists.`
- boundary_non_goals: `No manager exit-contract semantic change, no scan/backlog routing change, no claim that merge/retirement is complete before protected replay proves it.`
- residual_risk: `Canonical replay may still expose a downstream manager review or promotion seam after worker completion is finally consumed, but reconnect noise should no longer erase a valid worker_done contract.`
