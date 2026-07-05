# Issue: manager-delegated-continuation-stall-recovery-governance

- issue_id: `I-20260323-1705-A`
- title: Manager delegated continuation stall recovery governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-delegated-continuation-stall-recovery-governance`
- issue-name: `manager-delegated-continuation-stall-recovery-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260323/candidates.md#c-20260323-1705-a`
- source_brainstorm: `docs/B1-docs/raw-20260323/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/B2-docs/runtime/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md`
  - `docs/B2-docs/ibm/worker-active-reentry-for-manager-delegated-continuation-governance/issues/worker-active-reentry-for-manager-delegated-continuation-governance.md`
  - `docs/B2-docs/ibm/latest-manager-continuity-worker-consumption-governance/issues/latest-manager-continuity-worker-consumption-governance.md`
- pre_tests_path: `docs/B2-docs/ibm/manager-delegated-continuation-stall-recovery-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-manager-delegated-continuation-stall-recovery-governance.md`
- verification_artifact_dir: `docs/B2-docs/ibm/manager-delegated-continuation-stall-recovery-governance/code-reviews`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 已经具备 manager delegated continuation stall recovery 的基础 contract，但真实 dogfood 又暴露出两个新的 supervision false positive：

1. 旧 continuity 仍可能跨轮压住当前 delegated prompt 的 stall recovery。
2. 一条 active-busy worker 加一条 stale / missing prompt target，可能整体伪装成 lawful wait。

这会让 manager 在 `same-lane busy` 的合法等待态与真正需要 recovery 的坏态之间混淆，继续触发 `local_continuation_reentry` thrash，或者反过来压掉应有的恢复。

## Scope

1. 为 manager delegated continuation stall recovery 增加 idle-safe 分支，只在当前或更新 continuity 明确表达 lawful wait 时抑制 recovery。
2. 把 busy-wait helper 收紧为保守判断：
   - continuity 引用 stale runtime worktree refs 时失败；
   - worker prompt 缺失时失败；
   - target worktree 无法解析或不存在时失败。
3. 保持已有 recovery contract 不回退：
   - pending intake stall
   - new intake supersedes delegated prompt
   - unconsumed launchable worker prompt
   - mixed busy + launchable continuity
4. 用 focused regressions 锁住 same-round lawful wait、older continuity、busy+stale prompt、queued stale relaunch 等边界。

## Acceptance

- `same-lane busy` 的 lawful wait 只会在最新相关 continuity 上抑制 manager stall recovery。
- 较旧 continuity 不得跨轮压住当前 delegated continuation prompt 的 recovery。
- continuity 里若存在 stale runtime refs、缺失 worker prompt 或失效 target worktree，busy-wait helper 不得把它判成 lawful wait。
- mixed busy + launchable continuity 仍会触发 recovery。
- stale queued worker prompt 在 worker 已不运行时仍会重新变成 launchable 并被 relaunch。

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-active-worker-wait-does-not-recover`
- `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-mixed-busy-and-launchable-recovers`
- `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-older-busy-continuity-recovers`
- `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-busy-and-stale-prompt-recovers`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-queued-prompt`
- `docs/progress/workspace-routing-foundation/p-manager-delegated-continuation-stall-recovery-governance.md`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-active-worker-wait-does-not-recover`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-mixed-busy-and-launchable-recovers`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-older-busy-continuity-recovers`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-busy-and-stale-prompt-recovers`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-queued-prompt`
- manager/worker runtime regression batch around stall recovery, launch-state, semantic loop, worker reentry, and runtime recovery
- `docs/B2-docs/ibm/manager-delegated-continuation-stall-recovery-governance/code-reviews/20260328-manager-delegated-continuation-stall-recovery-verification.md`

## Next

- `2026-04-01 10:45 PDT` the narrow runtime repair is already present on `develop`; this owner is closed.
- Future work may deepen live post-merge dogfood acceptance or broader control-plane command semantics, but those belong to separate lifecycles rather than reopening this completed stall-recovery owner.
