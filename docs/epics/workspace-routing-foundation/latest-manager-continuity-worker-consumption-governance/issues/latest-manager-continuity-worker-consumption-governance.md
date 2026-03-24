# Issue: latest-manager-continuity-worker-consumption-governance

- issue_id: `I-20260322-0445`
- title: Latest manager continuity worker consumption governance
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `latest-manager-continuity-worker-consumption-governance`
- issue-name: `latest-manager-continuity-worker-consumption-governance`
- priority: P0
- source_candidate: `docs/pre-brainstorms/20260322-0445--latest-manager-continuity-worker-consumption/candidates.md#c-20260322-0445-a`
- source_brainstorm: `docs/pre-brainstorms/20260322-0445--latest-manager-continuity-worker-consumption/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/manager-continuation-handoff-consumption-governance/issues/manager-continuation-handoff-consumption-governance.md`
  - `docs/epics/workspace-routing-foundation/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md`
  - `docs/epics/workspace-routing-foundation/worker-active-reentry-for-manager-delegated-continuation-governance/issues/worker-active-reentry-for-manager-delegated-continuation-governance.md`

## Why

真实狗粮已经证明：

- `freely chat -> interruption resolution -> manager continuation` 已可达
- 主管可以产出合理的最新 worktree disposition
- 最新 worker prompt set 也能随最新 continuity 生成

但 runtime 仍可能继续消费更早一轮 delegated continuation。`manager-worker-launch-state.env` 也会停在旧 continuity，导致“主管已经给出更新监督结论，但 worker 没切到最新一轮执行输入”。

当前缺的不是新的 triage 语义，而是一个更硬的 runtime contract：

- latest manager continuity generated
- latest worker prompt set generated
- latest continuity / prompt set consumed by worker launch or reentry

## Scope

1. 定义 manager worker launch state 中 generated/consumed 的 canonical 字段。
2. 让 manager watchdog 在主管已运行时也持续尝试消费最新 continuity，而不是只在某些恢复路径才触发。
3. 让 worker launch / local reentry 始终以最新 continuity 派生的 prompt set 为准，而不是沿用旧 consumed marker。
4. 把这层 generated/consumed truth 暴露到 baseline/live status。
5. 补脚本级 integration tests，覆盖：
   - stale launch-state -> latest continuity consumption
   - manager watchdog already-running path 也会触发最新 continuity 消费
6. worker prompt contract 必须保持 runtime-launchable：
   - manager handoff 默认写 machine-readable `Worktree:` / `Branch:` header
   - runtime 在兼容期内也要能解析当前自然语言句式 `You are the worker for ... in ...`

## Acceptance

- 新 continuity 生成后，即使主管 supervisor 已在运行，watchdog 也会尝试消费最新 continuity。
- `manager-worker-launch-state.env` 记录：
  - latest continuity generated
  - latest continuity consumed
  - latest worker prompt set generated
  - latest worker prompt set consumed
- 若 worker 已活跃，reentry 走最新 prompt；若 worker 未运行，launch 走最新 prompt。
- `baseline-status` / `live-status` 能显示上述 generated/consumed truth。
- regression tests 覆盖：
  - stale continuity state 被更新到最新 continuity
  - `ensure_manager_once` 在 supervisor 已运行时仍会触发最新 continuity 消费

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
- `docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
- `docs/system/workspace/scripts/tests/test-freely-worker-prompt-natural-language-contract-compat`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/progress/workspace-routing-foundation/p-latest-manager-continuity-worker-consumption-governance.md`
- `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/code-reviews/20260322-latest-manager-continuity-worker-consumption-verification.md`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
- `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
- `./bin/governance-check`

## Next

- 当前 pre-merge verification 已完成。
- 仍需 merge 后在 `develop` 上做一次真实 `freely chat` post-merge acceptance，确认最新 manager continuity 会被 worker runtime 消费。
