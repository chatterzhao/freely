# Verification: runtime-daemon-self-loop-followthrough-governance active authoritative worker prompt consumption

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-24`
- verifier: `codex`
- source_branch: `feature/manager-active-worker-prompt-consumption-reconcile-20260424`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-manager-active-worker-prompt-consumption-reconcile`

## Scope Verdict

- `FAIL`: canonical `develop` continuity-first replay still failed the autonomy loop after the frozen-prompt repair because manager could keep the exact authoritative retained-lane prompt in queued state even while that same worker lane was already active on it.
- `PASS`: the real seam sat inside manager launch bookkeeping, not task-source selection. Replay state showed `ACTIVE_RUNNING_WORKER_COUNT="1"` while `LAST_MANAGER_WORKER_PROMPTS_CONSUMED=""` and `QUEUED_WORKER_PROMPTS` still named the authoritative prompt, so runtime kept seeing self-created queue pressure instead of a waitable active worker.
- `PASS`: runtime now recognizes an active worker whose authoritative prompt path exactly matches the manager prompt and treats that prompt as already consumed/launched for continuity and launch-state purposes.
- `PASS`: delegated-continuation busy workers remain queued. The new shortcut explicitly excludes `worker_project_busy_with_delegated_continuation()`, so this fix does not collapse the existing busy-worker queue discipline.
- `PASS`: focused regressions cover both sides of the boundary: active authoritative workers are consumed and waited on, while delegated busy workers still queue.
- `PENDING`: guarded premerge and canonical `develop` daemon replay still need to prove the retained lane finishes, retires, and hands control back to scan-selected backlog without another same-prompt churn seam.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-active-authoritative-worker-consumes-prompt`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-busy-worker-queue`
3. `bash docs/system/workspace/scripts/tests/test-freely-manager-launch-state-refresh-supersedes-queued-prompt-with-manager-continuity`
4. `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption-current-format`

## Implementation Decision Note

- decision: `Treat an already-active worker's exact authoritative prompt as consumed manager launch state instead of keeping it queued.`
- why_this: `Canonical replay had already selected the correct retained lane. The blocker was that launch bookkeeping could not distinguish “this prompt is already the active authoritative worker” from “this prompt still needs a new worker launch,” so manager kept churning around its own selected worker instead of waiting for it.`
- alternatives_considered: `Always clear queued prompts whenever any worker is active; move prompt-consumption truth back into manager-only artifacts; treat all busy workers as auto-consumed.`
- boundary_non_goals: `No scan-json policy change, no continuity-first downgrade, no relaxation for delegated busy worker queueing, and no claim that full daemon autonomy is complete before canonical replay lands.`
- residual_risk: `Canonical replay may still expose a later worker closeout, merge, or retirement seam after this queue/bookkeeping boundary is fixed, but the active authoritative prompt should no longer be mistaken for an unconsumed queue item.`
