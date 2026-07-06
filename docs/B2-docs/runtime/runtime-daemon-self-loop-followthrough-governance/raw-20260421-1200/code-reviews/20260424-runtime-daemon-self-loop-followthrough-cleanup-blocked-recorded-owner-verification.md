# Verification: runtime-daemon-self-loop-followthrough-governance cleanup blocked recorded-owner followthrough

- issue_id: `I-20260421-1200-A`
- date: `2026-04-24`
- scope: `Verify that a blocked cleanup worker keeps authoritative recorded ownership when its latest worker AI prompt no longer carries machine-readable dispatch headers.`

## Findings

- `FAIL`: canonical `develop` replay proved one more retained-cleanup seam after the pre-stop continuation fix. A cleanup worker could exit lawfully with `EXIT_KIND=worker_blocked`, yet manager restart still relaunched the same cleanup target because ownership lookup read the latest worker AI prompt instead of the verification-contract source prompt.
- `PASS`: intent-signature recovery now uses `status_intent_prompt_file_for_project()`, so blocked-worker ownership stays anchored to the delegated source prompt preserved by the worker verification contract.
- `PASS`: focused regression coverage now matches the real runtime shape where the latest worker AI prompt lacks `Worktree:` / `Branch:` headers, and duplicate cleanup launch requests correctly queue behind the blocked recorded owner instead of relaunching.

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-cleanup-queue-recorded-owner-from-verification-contract`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-stale-existing-worktree-blocked`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-duplicate-promotion-queue-recorded-owner`
- `./bin/pretests-gate --project /Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260424-feature-cleanup-worker-blocked-consumption-boundary --issue /Users/zhaoyu/Downloads/code/my-freely/freely/docs/B2-docs/runtime/runtime-daemon-self-loop-followthrough-governance/issues/runtime-daemon-self-loop-followthrough-governance.md`
- `./bin/governance-check`

## Status

- `PASS`: blocked cleanup workers now retain authoritative recorded ownership through the verification-contract source prompt boundary.
- `PENDING`: protected premerge replay, guarded `develop` merge, and canonical daemon self-host replay still need to prove the retained cleanup lane is consumed once and Freely returns to scan-driven next-task routing.

## Implementation Decision Note

- decision: `Derive current blocking intent from the status/verification-contract prompt source instead of the latest worker AI prompt artifact.`
- why_this: `Runtime ownership and blocker consumption need the same authoritative prompt truth worker launch and recovery already consume; the latest AI prompt is an execution artifact and can legally drop machine-readable dispatch headers.`
- alternatives_considered: `Keep latest-prompt lookup and force every worker AI prompt to retain dispatch headers; persist a second ownership signature file just for blocked cleanup recovery; special-case retained cleanup lanes only.`
- boundary_non_goals: `No scan-priority redesign, no broader cleanup-governance rewrite, and no claim that canonical develop end-to-end autonomy is already complete.`
- residual_risk: `Canonical develop may still expose a later cleanup-consumption or retirement seam after this ownership fix lands, but the blocked-worker recorded-owner boundary is now aligned with verification-contract truth.`
