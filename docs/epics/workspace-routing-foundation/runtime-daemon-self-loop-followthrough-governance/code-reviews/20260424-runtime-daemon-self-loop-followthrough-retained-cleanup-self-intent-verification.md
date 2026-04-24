# Code Review: runtime-daemon-self-loop-followthrough-governance

- date: `2026-04-24 01:18 PDT`
- reviewer: `codex`
- branch: `feature/manager-worker-launch-self-conflict-boundary-20260424`
- worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-manager-worker-launch-self-conflict-boundary`

## Scope

- Prove the canonical retained cleanup worker stall is a manager-side self-conflict inside `manager_runtime_launch_workers_from_latest_handoff()`, not a scan-json routing miss or a worker bootstrap failure.
- Keep the duplicate blocked-owner queue behavior intact while allowing the merged retained cleanup lane to relaunch itself lawfully.

## Findings

- Real canonical runtime evidence showed `manager_exit_contract_delegate_workers` firing for `/Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260424-005222-worker-runtime-cleanup-followthrough-hygiene-codex.txt`, with `worker_prompt_launchable_for_manager_project => yes`, while `queued_worker_prompts` remained populated and `active_running_worker_count=0`.
- Direct helper probes proved `launch_worker_from_manager_prompt_if_needed` succeeded for that prompt and wrote worker intake / verification state, so the failure boundary was the manager queue-selection gate rather than worker startup.
- The launch loop was preloading `selected_intent_signatures_csv` from recorded worker ownership. For the retained cleanup lane, that recorded signature was the same `cleanup@<target_worktree>` signature as the queued authoritative manager prompt, so manager self-queued forever even though no other worker owned the lane.
- The repair adds a bounded reclaim rule only for cleanup prompts with verification metadata whose target is the same retained merged lane already carrying that recorded signature.
- The pre-existing duplicate-owner queue case still blocks, so the repair does not widen ownership beyond the retained merged cleanup relaunch seam.

## Commands

- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reclaims-retained-merged-cleanup-self-intent`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-cleanup-queue-recorded-owner-from-verification-contract`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-queued-prompt`

## Verdict

- `PASS`: retained merged cleanup self-intent relaunch now launches.
- `PASS`: duplicate cleanup recorded-owner queue behavior remains blocked.
- `PASS`: stale queued non-conflicting relaunch behavior remains intact.
