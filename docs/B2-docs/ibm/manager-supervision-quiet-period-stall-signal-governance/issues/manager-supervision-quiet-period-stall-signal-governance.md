# Issue: manager-supervision-quiet-period-stall-signal-governance

- issue_id: `I-20260328-0335-A`
- title: Manager supervision quiet-period stall-signal governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-supervision-quiet-period-stall-signal-governance`
- issue-name: `manager-supervision-quiet-period-stall-signal-governance`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260328-0335/candidates.md#c-20260328-0335-a`
- source_brainstorm: `docs/B1-docs/raw-20260328-0335/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/manager-delegated-continuation-stall-recovery-governance/issues/manager-delegated-continuation-stall-recovery-governance.md`
  - `docs/epics/workspace-routing-foundation/watchdog-restart-storm-and-process-churn-governance/issues/watchdog-restart-storm-and-process-churn-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-delegated-intake-absorption-closure-governance/issues/manager-delegated-intake-absorption-closure-governance.md`
- pre_tests_path: `docs/epics/workspace-routing-foundation/manager-supervision-quiet-period-stall-signal-governance/pre-tests.md`
- progress_path: `docs/progress/workspace-routing-foundation/p-manager-supervision-quiet-period-stall-signal-governance.md`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/manager-supervision-quiet-period-stall-signal-governance/code-reviews`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

`I-20260323-1705-A` 已经把 manager delegated continuation stall recovery 收紧到 `same-lane busy` 的 lawful wait 边界，但真实 dogfood 继续暴露出更深一层的问题：

- manager 与 active worker 都存活
- delegated continuation 已进入当前 manager prompt
- `pending_delegated_continuation_ids` 已清空
- 但 manager 只要在监督轮次里静默约 `90s`，runtime 仍会触发
  - `runtime-stalled-ai-recovery`
  - `local_continuation_reentry`
  - `operator_stop_requested`

这说明当前 stall detector 仍把 delegated-supervision quiet-period 近似成强 stall 证据。三个 loop 的设计并不要求 manager 在监督 active worker 时必须持续产生新的 `cycle log` 字节，因此该行为更像 runtime heartbeat contract 过粗，而不是产品需求要求的 stop/restart 语义。

## Scope

1. 为 manager delegated-supervision quiet-period 定义 runtime-owned signal contract，区分：
   - 合法 supervision-only 静默
   - 真 stalled manager round
2. 补足负向测试，冻结：
   - `active manager + active worker + delegated supervision quiet-period`
   - 不得直接进入 `local_continuation_reentry`
3. 评估并落最小修法：
   - delegated-supervision idle-safe contract
4. 保持已有 stall recovery 真阳性不退化：
   - pending intake stall
   - new intake supersedes delegated prompt
   - stale / launchable worker prompt
   - worker runtime missing
5. 把 restart-storm contract 复核与 runtime-owned recovery stop observability 区分保留为 follow-on，不阻塞本 issue 的最小行为修复收口。

## Non-Goals

1. 不全局调大 `MANAGER_AI_STALL_THRESHOLD_SECS` 作为首选修法。
2. 不关闭 delegated continuation stall recovery 总体能力。
3. 不在本 issue 中重写 delegated backlog absorption 全部生命周期；那是并行证据面，不应阻塞 primary owner。
4. 不把 CLI/TUI/GUI observability 产品面扩张回本 issue。

## Acceptance

1. 当 manager 处于 delegated-supervision quiet-period 且 worker/runtime truth 仍健康时，runtime 不得仅凭 `cycle log/prompt mtime > threshold` 直接触发 `local_continuation_reentry`。
2. 当存在更强 stall 证据时，已有 recovery 仍然生效，不得因新 idle-safe 分支而放过真 stall。
3. regression 至少覆盖：
   - quiet-period lawful wait 不恢复
   - unrelated active worker 不得错误 suppress recovery
   - active but non-busy worker 不得错误 suppress recovery
   - quiet-period + stronger stall evidence 仍恢复

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-quiet-period-does-not-recover`
- `docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-unrelated-active-worker-recovers`
- `docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-nonbusy-worker-recovers`
- `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-mixed-busy-and-launchable-recovers`
- `docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-busy-and-stale-prompt-recovers`
- `docs/progress/workspace-routing-foundation/p-manager-supervision-quiet-period-stall-signal-governance.md`
- `docs/epics/workspace-routing-foundation/manager-supervision-quiet-period-stall-signal-governance/code-reviews/20260328-manager-supervision-quiet-period-stall-signal-verification.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-quiet-period-does-not-recover`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-unrelated-active-worker-recovers`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-supervision-nonbusy-worker-recovers`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-active-worker-wait-does-not-recover`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-older-busy-continuity-recovers`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-mixed-busy-and-launchable-recovers`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-delegated-continuation-busy-and-stale-prompt-recovers`

## Next

- `2026-03-30 17:34 PDT` the minimal behavior repair and verification closeout are already absorbed by `develop` commit `82ea1e6`, with canonical evidence in `docs/epics/workspace-routing-foundation/manager-supervision-quiet-period-stall-signal-governance/code-reviews/20260328-manager-supervision-quiet-period-stall-signal-verification.md`.
- Restart-storm revalidation or broader observability changes remain follow-on work and must open their own lifecycle if they need implementation.
