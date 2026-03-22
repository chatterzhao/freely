# Code Review: latest-manager-continuity-worker-consumption-governance

## Result

- pre-merge verification passed

## Evidence

- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
- `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
- `./bin/governance-check`

## What Changed

1. `ensure_manager_once` now invokes worker latest-continuity consumption even when the manager supervisor is already running.
2. `manager-worker-launch-state.env` now records:
   - latest continuity generated
   - latest continuity consumed
   - latest worker prompts generated
   - latest worker prompts consumed
3. baseline/live status now expose the generated/consumed launch-state truth.
4. stale continuity snapshots are reset when a newer continuity file becomes canonical.

## Remaining Acceptance

- run one real post-merge acceptance on `develop` via `freely chat`, confirming workers consume the newest manager continuity round in a live dogfooding loop.
