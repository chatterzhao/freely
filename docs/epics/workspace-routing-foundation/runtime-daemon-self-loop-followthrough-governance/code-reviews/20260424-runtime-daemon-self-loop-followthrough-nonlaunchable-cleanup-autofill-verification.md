# Verification: runtime-daemon-self-loop-followthrough-governance nonlaunchable cleanup prompt autofill

- issue_id: `I-20260421-1200-A`
- date: `2026-04-24`
- scope: `Verify that canonical cleanup_governance replay can recover when manager continuity already contains an AI-written retained-lane worker prompt, but that prompt is nonlaunchable because it lacks the verification metadata required for an absorbed merged cleanup lane.`

## Findings

- `FAIL`: canonical `develop` replay at `2026-04-24 00:47:41 PDT` proved the earlier recorded-owner repair was not enough. Manager now scanned `manager-task-source-scan-latest.json`, selected the retained dirty cleanup lane, and wrote fresh continuity plus worker prompt, but the prompt was plain hygiene text without verification metadata. Because the target worktree branch was already merged into `develop`, `worker_prompt_launchable_for_manager_project()` correctly rejected it and runtime looped on `manager_exit_contract_invalid details=WORKER_PROMPTS_NOT_LAUNCHABLE`.
- `PASS`: cleanup-governance retirement handoff detection no longer stops merely because continuity already mentions a worker prompt. If the existing prompt set is still nonlaunchable for the manager project, runtime now materializes the authoritative cleanup followthrough prompt from continuity and owner-issue truth instead of accepting the dead-end AI prompt as final.
- `PASS`: the repair preserves the launch gate itself. Impossible `delegate_workers` contracts are still rejected unless at least one prompt is actually launchable; the new behavior only adds the missing authoritative prompt when cleanup_governance continuity proves that retained merged-lane followthrough is still required.

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-autodelegates-cleanup-when-existing-prompt-is-nonlaunchable`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-autodelegates-canonical-cleanup-continuity`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-exit-contract-delegate-workers-requires-launchable-prompt`

## Status

- `PASS`: cleanup_governance continuity can now recover from a nonlaunchable retained-lane AI prompt by materializing an authoritative verification-bound cleanup prompt and updating the delegate-workers contract to something runtime can actually launch.
- `PENDING`: guarded premerge replay, guarded `develop` merge, and canonical daemon replay still need to prove the real cleanup worker launches, closes the retained lane lawfully, and Freely continues to the next scan-selected task.

## Implementation Decision Note

- decision: `Treat existing cleanup_governance worker prompts as sufficient only when at least one is launchable for the current manager project; otherwise materialize the authoritative cleanup followthrough prompt from continuity.`
- why_this: `The AI-written prompt is useful as evidence of manager judgement, but retained merged cleanup lanes need verification-bound prompt metadata before runtime may lawfully relaunch them.`
- alternatives_considered: `Relax the merged-lane launch gate; require the AI prompt itself to always carry full verification metadata; discard the existing AI prompt and silently overwrite continuity.`
- boundary_non_goals: `No change to scan-source ranking, no relaxation of launchability validation, and no claim that canonical develop end-to-end autonomy is already complete.`
- residual_risk: `Canonical replay may still expose a later cleanup execution or retirement seam after the worker finally launches, but the dead-end nonlaunchable-prompt loop is now closed.`
