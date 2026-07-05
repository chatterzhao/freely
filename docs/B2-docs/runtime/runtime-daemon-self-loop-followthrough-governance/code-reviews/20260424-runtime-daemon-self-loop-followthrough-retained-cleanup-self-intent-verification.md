# Verification: runtime-daemon-self-loop-followthrough-governance retained cleanup self-intent relaunch

- issue_id: `I-20260421-1200-A`
- issue_path: `docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- verification_date: `2026-04-24`
- verifier: `codex`
- source_branch: `feature/manager-worker-launch-self-conflict-boundary-20260424`
- source_worktree: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-manager-worker-launch-self-conflict-boundary`

## Scope Verdict

- `FAIL`: canonical `develop` still stalled after the nonlaunchable cleanup autofill repair. Manager emitted `manager_exit_contract_delegate_workers`, the retained cleanup prompt stayed launchable, and `active_running_worker_count` still remained `0`, so the seam had moved past prompt materialization into worker launch selection itself.
- `PASS`: direct helper probes proved `launch_worker_from_manager_prompt_if_needed` already succeeded for the canonical retained cleanup prompt, so the blocker was not scan-json routing or worker bootstrap.
- `PASS`: the real boundary was manager-side self-conflict. `manager_runtime_launch_workers_from_latest_handoff()` preloaded `selected_intent_signatures_csv` from recorded worker ownership, then self-queued the retained merged cleanup lane because the authoritative prompt carried the same `cleanup@<target_worktree>` signature as the lane's stale recorded ownership.
- `PASS`: runtime now allows a bounded reclaim path only when a cleanup prompt with verification metadata targets that same retained merged lane and its current recorded signature exactly matches the prompt signature.
- `PASS`: adjacent duplicate-owner queue behavior remains intact, so this repair does not widen ownership beyond the retained cleanup self-relaunch seam.
- `PENDING`: canonical `develop` still needs guarded promote plus real daemon replay proving the worker launches, closes or classifies the retained cleanup lane lawfully, and Freely advances to the next scan-selected task.

## Commands

1. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reclaims-retained-merged-cleanup-self-intent`
2. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-cleanup-queue-recorded-owner-from-verification-contract`
3. `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-queued-prompt`
4. `bash docs/system/workspace/scripts/tests/test-freely-manager-launches-workers-after-ai-cycle`
5. `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-manager-worker-launch-self-conflict-boundary --issue /Users/zhaoyu/Downloads/code/my-freely/freely/docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
6. `./bin/governance-check`

## Implementation Decision Note

- decision: `Let the retained merged cleanup worker reclaim its own recorded cleanup intent during manager relaunch when the authoritative verification-bound prompt is targeting that same lane.`
- why_this: `The canonical stall happened after prompt generation and launchability validation, so broadening scan priority or rewriting worker startup would miss the real seam. The narrow fix is to stop treating the retained lane's own recorded cleanup signature as a foreign conflict when manager is intentionally relaunching that exact cleanup worker.`
- alternatives_considered: `Keep the recorded-owner conflict absolute and hope later patrols clear it; strip recorded cleanup ownership more broadly before launch; bypass ownership checks for every merged-lane cleanup prompt.`
- boundary_non_goals: `No scan-json task-source redesign, no general ownership conflict relaxation, no broader cleanup-governance rewrite, and no claim that canonical daemon looping is fully accepted before develop replay completes.`
- residual_risk: `After this self-conflict seam is removed, canonical replay may still expose a later retained-lane closeout or retirement blocker, but worker launch selection itself is now bounded and covered.`
