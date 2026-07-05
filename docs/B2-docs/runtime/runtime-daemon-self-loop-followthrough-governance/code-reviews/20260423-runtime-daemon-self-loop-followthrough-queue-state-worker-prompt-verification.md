# Verification: runtime-daemon-self-loop-followthrough-governance queue-state worker prompt launch followthrough

- issue_id: `I-20260421-1200-A`
- date: `2026-04-23`
- scope: `Keep current ## Queue State worker_prompts handoffs launchable so manager delegate_workers actually materializes worker launch state and starts the selected cleanup lane.`

## Findings

- `FAIL`: canonical `develop` replay re-delegated the retained cleanup lane with a lawful `delegate_workers` contract, but `manager-worker-launch-state.env` still showed no generated, queued, or launched worker prompt.
- `FAIL`: runtime only parsed prompt paths from direct `## Worker Delegation` handoffs and missed the current `## Queue State` shape where `worker_prompts:` is the authoritative launchable list.
- `PASS`: queue-state continuity parsing now accepts both bare `worker_prompts:` and list-item `- worker_prompts:` forms, so manager launch-state reconciliation and post-cycle launch consume the same continuity truth that exit-contract validation already approved.
- `PASS`: post-cycle manager launch now starts one worker under the queue-state handoff shape instead of returning `launched_count=0`.

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-manager-continuity-current-worker-prompt-parsing`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`
- `bash -lc 'source docs/system/workspace/scripts/runtime/freely; latest_manager_worker_prompt_csv_from_continuity /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260423-235503.md'`

## Status

- `PASS`: runtime can now extract the retained cleanup worker prompt from the same queue-state continuity shape that canonical replay emitted on `develop`.
- `PASS`: the focused post-cycle launch regression proves manager now records launch-state truth and starts the selected worker instead of silently consuming `delegate_workers`.
- `PENDING`: guarded premerge and canonical `develop` replay still must prove this repair closes the retained cleanup lane, retires it lawfully, and lets manager continue to the next scan-selected task.

## Implementation Decision Note

- decision: `Extend the existing continuity parser to cover the current queue-state handoff shape rather than inventing a second launch-state recovery path.`
- why_this: `The defect was not worker startup itself; it was that the parser feeding launch-state reconciliation and post-cycle launch dropped prompt paths from a continuity format manager was already writing in production.`
- alternatives_considered: `Special-case delegate_workers to reread manager-exit-contract.env only; rewrite manager continuity back to older Worker Delegation-only shape; synthesize launch-state from runtime-events instead of continuity truth.`
- boundary_non_goals: `No scan-ranking redesign, no new cleanup-governance owner, and no relaxation of the requirement that launchability stays derived from continuity plus prompt metadata.`
- residual_risk: `Canonical replay may still expose a narrower cleanup/retirement seam after the worker finally launches, but this repair removes the prompt-drop that previously prevented any worker execution at all.`
