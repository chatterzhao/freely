# Verification: runtime-daemon-self-loop-followthrough-governance terminal handoff slot collapse

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-25`
- verifier: `codex`
- source_branch: `feature/runtime-target-worker-role-and-starting-stuck-recovery-20260424`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-runtime-target-worker-role-and-starting-stuck-recovery`

## Scope Verdict

- `FAIL`: canonical `develop` replay after merge commit `2fd905c9` disproved the earlier implicit "already finished" assumption. Root runtime no longer lost worker role or `starting`-stuck recovery, but it still kept `ACTIVE_RUNNING_WORKER_COUNT="1"` after the delegated `test-pre-merge` target had already emitted terminal `EXIT_KIND="worker_handoff_needed"` truth and materialized the next local followthrough prompt. That stale count kept the old outer prompt suppressed as if an active worker still existed, so manager kept redelegating the same old prompt instead of consuming the handoff continuation.
- `PASS`: the bounded seam sits inside manager launch-state reconciliation, not in agent/skill naming. Runtime already treats manager/worker control as artifact-driven: manager writes delegation artifacts, runtime launches the next lane, and worker exit contracts decide whether control returns, delegates again, or closes out. The remaining bug was that prompt-liveness reconciliation pruned the dead/terminal launched prompt but then immediately rewrote `ACTIVE_RUNNING_WORKER_COUNT` from the stale launch-state hint.
- `PASS`: `manager_worker_launch_state_reconcile_prompt_liveness()` now collapses that hint back to the actually discovered worker count when the current continuity's launched prompt set has been fully pruned. This keeps the old hint behavior for genuinely active delegated lanes, but stops terminal-handoff or reclaimed slots from pinning `ACTIVE_RUNNING_WORKER_COUNT` forever.
- `PASS`: focused regressions passed for the exact seam and adjacent recovery surface:
  1. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-collapses-terminal-handoff-worker-slot`
  2. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-reclaims-stale-starting-worker-slot`
  3. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
  4. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-malformed-verification-contract`
  5. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-without-verification-contract`
  6. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-while-worker-active`
- `PENDING`: guarded replay and canonical `develop` daemon replay still must prove this collapse is enough for the retained premerge handoff chain to advance through real task completion, lawful merge/retirement, and next-task patrol without manual intervention.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-collapses-terminal-handoff-worker-slot`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-path-reclaims-stale-starting-worker-slot`
3. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery`
4. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-malformed-verification-contract`
5. `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-blocks-without-verification-contract`
6. `bash docs/system/workspace/scripts/tests/test-freely-ensure-manager-keeps-supervisor-while-worker-active`

## Implementation Decision Note

- decision: `Collapse stale launch-state active-worker hints only when prompt-liveness reconciliation has already pruned the current continuity's launched prompt set to empty.`
- why_this: `The real control-plane need for the hint still exists while a delegated non-worker branch target is genuinely active, but once reconciliation has already proven there is no surviving launched prompt for the current continuity, preserving the larger hint only recreates the same false wait state forever.`
- alternatives_considered: `Remove the hint globally from semantic-loop worker counting; teach worker discovery to count test-pre-merge branches as ordinary workers; special-case worker_handoff_needed in manager recovery only.`
- boundary_non_goals: `No new role taxonomy, no broad semantic-loop redesign, and no claim that canonical develop acceptance is complete before the full daemon loop closes one task and advances to the next.`
- residual_risk: `This change only closes the stale active-worker-count seam; canonical develop may still expose a later manager followthrough or merge/retire sequencing gap before the full unattended loop is complete.`
