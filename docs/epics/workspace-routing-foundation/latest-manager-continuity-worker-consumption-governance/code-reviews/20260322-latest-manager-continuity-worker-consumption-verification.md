# Code Review: latest-manager-continuity-worker-consumption-governance

## Result

- pre-merge verification passed
- 2026-03-23 worker continuation reran the same verification suite and kept the issue in `in_verification`; only protected-environment post-merge acceptance remains.
- 2026-03-23 first-hop closure rechecked `lead-agent -> constitution-guard -> laws-enforcer -> context-source-skill`, confirmed this intake is still a `continuation` routed to `dev-loop-execution`, and found no new implementation gap beyond the existing post-merge acceptance requirement.
- 2026-03-23 second-hop dev-loop continuation revalidated the runtime/test truth source for delegated continuation active-prompt visibility and reran the full targeted suite; all checks remained green, so this lane still needs only post-merge `develop` acceptance.
- 2026-03-23 direct runtime inspection confirmed why the visibility regression is closed: `freely` persists consumed delegated ids immediately after prompt build, filters those ids out of active pending snapshots while the same prompt is running, and exposes them again after AI exit.
- 2026-03-23 current worker continuation reran the full targeted suite once more from the clean feature worktree and rechecked the runtime truth source, confirming the route is still `continuation -> dev_loop -> codex` and the lane remains verification-only.

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
- `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
- `./bin/governance-check`
- runtime truth-source checkpoints in `docs/system/workspace/scripts/runtime/freely`:
  - `LAST_DELEGATED_CONTINUATION_CONSUMED_IDS` / `..._AT` persistence
  - `active_prompt_consumed_delegation_ids_for_project`
  - `delegated_continuation_snapshot_for_project`
  - `delegated_continuation_ids_for_project`

## What Changed

1. `ensure_manager_once` now invokes worker latest-continuity consumption even when the manager supervisor is already running.
2. `manager-worker-launch-state.env` now records:
   - latest continuity generated
   - latest continuity consumed
   - latest worker prompts generated
   - latest worker prompts consumed
3. baseline/live status now expose the generated/consumed launch-state truth.
4. stale continuity snapshots are reset when a newer continuity file becomes canonical.
5. delegated continuation ids are now treated as consumed as soon as they are absorbed into the active prompt, so live status hides them from pending until the active AI exits.
6. the active-prompt visibility contract remained stable under repeated worker continuation reruns; no new implementation delta was needed in this lane.

## Remaining Acceptance

- run one real post-merge acceptance on `develop` via `freely chat`, confirming workers consume the newest manager continuity round in a live dogfooding loop.
- keep this feature worktree scoped to verification writeback only until that `develop` acceptance is recorded.
