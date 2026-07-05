# Pre-test-merge semantic audit and recovery

## Compatibility Note

- 历史 audit/path 保留 `pre-test-merge` 命名，避免破坏既有引用。
- 当前 canonical 语义已经升级为 `test-pre-merge-*` 测试批次前缀族。
- 下文出现的 `pre-test-merge` 都按 `test-pre-merge-*` 前缀族理解。

## Context

This audit compares the pre-test-merge-only history against the current `develop` branch, centered on:

- `61121e1` `feat: consume latest manager continuity for workers`
- `9f4f8a6` `docs: add latest manager continuity consumption prebrainstorm`
- `99c21af` `docs: add pre-test-merge acceptance stall prebrainstorm`

Goal:

- preserve useful capability
- avoid regressions
- decide what should be recovered into Freely as a capability instead of being copied back mechanically

## Current develop evidence

The current `develop` branch already contains the core runtime path for latest-manager-continuity driven worker launch and reentry:

- [`docs/system/workspace/scripts/runtime/freely`](../../system/workspace/scripts/runtime/freely#L1524) writes launch state with `LAST_MANAGER_CONTINUITY_CONSUMED` and `LAUNCHED_WORKER_PROMPTS`
- [`docs/system/workspace/scripts/runtime/freely`](../../system/workspace/scripts/runtime/freely#L1580) resolves the latest manager continuity file
- [`docs/system/workspace/scripts/runtime/freely`](../../system/workspace/scripts/runtime/freely#L1665) converts a manager prompt into a delegated worker intake or local continuation reentry
- [`docs/system/workspace/scripts/runtime/freely`](../../system/workspace/scripts/runtime/freely#L1682) consumes all prompts from the latest continuity file
- [`docs/system/workspace/scripts/runtime/freely`](../../system/workspace/scripts/runtime/freely#L2144) still provides manager recovery that calls the latest-handoff launcher
- [`docs/system/workspace/agents/manager-agent.md`](../../system/workspace/agents/manager-agent.md#L40) now routes delegated owners back into the next restart-point decision
- [`docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`](../../system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage#L97) and [`docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`](../../system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch#L113) already assert the launch/reentry path

## Semantic audit matrix

### Already absorbed by `develop`

- The core behavior from `61121e1` that turns the latest manager continuity into worker continuation launch is already present in `develop`.
- Worker reentry for active delegates is already covered by current tests and runtime behavior.
- The manager routing docs already reflect the "delegate, then re-decide restart point" contract.

### Still missing and worth recovering

- The `99c21af` concern is not about runtime mechanics; it is about `pre-test-merge` lifecycle governance.
- We still need a Freely capability that can recognize stale or misused pre-test-merge batches, treat them as a bounded validation batch, and force explicit retirement or re-creation when the batch is no longer authoritative.
- That lifecycle capability should be materialized as Freely governance, not as a manual convention.

### Obsolete or superseded

- The extra `61121e1` launch-state bookkeeping fields that exposed generated-vs-consumed continuity snapshots are no longer the current truth surface.
- The old `live-status` and `baseline-status` echo of manager continuity bookkeeping was removed in later `develop` history and should not be reintroduced without a new verification reason.
- The `9f4f8a6` prebrainstorm is superseded as a standalone discovery artifact by later continuity-handoff and runtime-linkage workstreams in `develop`.

### Needs more verification

- Whether the launch-state file should remain a narrow consumed-prompt ledger or regain richer observability.
- Whether `pre-test-merge` needs first-class batch freshness metadata in runtime status, or whether the governance signal should live only in docs and patrol logic.
- Whether the recovered capability should be implemented as a runtime/status feature, a branch-management skill enhancement, or both.

## Recovery policy

- Keep the runtime launch/reentry behavior already present in `develop`.
- Do not cherry-pick the old launch-state observability back just because it existed in `61121e1`.
- Recover the `pre-test-merge` lifecycle question as a Freely governance capability.
- Treat this audit as the source of the next pre-brainstorm/candidate split, not as permission to edit runtime code yet.

## Lifecycle closure

- This audit no longer owns a separate implementation path.
- Its governance conclusion is now absorbed by:
  - `docs/B2-docs/ibm/pre-test-merge-responsibility-usage-and-lifecycle-governance/issues/pre-test-merge-responsibility-usage-and-lifecycle-governance.md`
- This worktree remains only as supporting semantic evidence for that governance lifecycle.
- Once the absorption writeback is committed, this branch should be treated as `retire-ready` unless a new audit-specific gap appears.
