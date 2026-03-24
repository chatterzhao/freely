# Issue: latest-manager-continuity-worker-consumption-governance

- issue_id: `I-20260322-0445`
- title: Latest manager continuity worker consumption governance
- phase_state: `completed`
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
7. 若同一 continuity 的 prompt 曾被记录为 consumed，但对应 worker 当前并未运行，runtime 必须把它视为 stale consumed state，并允许重新 launch / reentry，而不是要求先生成一轮新的 continuity。
8. 当 delegated continuation 已被当前活跃 prompt 吸收时，runtime 必须在 cycle completion 之前就把 consumed truth 写入 session state / live-status，并从实时 pending 视图中剔除这些 ids；但若当前 AI 已退出，这些 ids 必须重新回到 pending 视图，供 recovery 继续接管。

## Acceptance

- 新 continuity 生成后，即使主管 supervisor 已在运行，watchdog 也会尝试消费最新 continuity。
- `manager-worker-launch-state.env` 记录：
  - latest continuity generated
  - latest continuity consumed
  - latest worker prompt set generated
  - latest worker prompt set consumed
- 若 worker 已活跃，reentry 走最新 prompt；若 worker 未运行，launch 走最新 prompt。
- 若 worker 已停止，但当前 continuity / prompt set 仍是最新真相，runtime 会忽略 stale consumed marker 并重新 launch。
- 若 delegated continuation 已进入当前活跃 prompt，`live-status` 会立刻显示 consumed ids，并且不会再把同一批 ids 同时显示为 pending；当前 AI 停止后，这些 ids 会重新回到 pending 视图。
- 若 latest manager continuity 把 lane 明确放进 `Frozen Queue` / `desired-frozen`，runtime 不会再把该 prompt 计入 launchable generated/consumed inventory，也不会因 stale-consumed 或 worker local `DESIRED_RUNTIME_STATE=running` 而把该 lane 自动 relaunch / recovery。
- 若旧 launch-state csv 里还残留同一 continuity 下已被冻结的 prompt，下一轮 reconcile 会先按当前 continuity 的 launchable prompt set 清掉这些 stale frozen entries，再决定是否对仍 launchable 的 prompt 做 relaunch。
- `baseline-status` / `live-status` 能显示上述 generated/consumed truth。
- regression tests 覆盖：
  - stale continuity state 被更新到最新 continuity
  - `ensure_manager_once` 在 supervisor 已运行时仍会触发最新 continuity 消费
  - frozen-only prompt 不进入 launch/relaunch inventory
  - same-continuity stale frozen prompt 会从 launch-state consumed/launched csv 中被清掉
  - manager recovery 不会复活 latest continuity 已冻结的 worker lane

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
- `docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-frozen-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reconciles-stale-frozen-consumed-prompt`
- `docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-frozen-worker`
- `docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
- `docs/system/workspace/scripts/tests/test-freely-live-status`
- `docs/system/workspace/scripts/tests/test-freely-worker-prompt-natural-language-contract-compat`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/progress/workspace-routing-foundation/p-latest-manager-continuity-worker-consumption-governance.md`
- `docs/epics/workspace-routing-foundation/latest-manager-continuity-worker-consumption-governance/code-reviews/20260322-latest-manager-continuity-worker-consumption-verification.md`

## Verification

- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `bash docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
- `bash docs/system/workspace/scripts/tests/test-freely-latest-manager-continuity-worker-consumption`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-relaunches-stale-consumed-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-skips-frozen-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-reconciles-stale-frozen-consumed-prompt`
- `bash docs/system/workspace/scripts/tests/test-freely-manager-runtime-recovery-skips-frozen-worker`
- `bash docs/system/workspace/scripts/tests/test-freely-delegated-continuation-active-prompt-visibility`
- `bash docs/system/workspace/scripts/tests/test-freely-live-status`
- `./bin/governance-check`

## Next

- 2026-03-24 canonical `develop` post-merge acceptance is now recorded as `pass`. During manager patrol, `live-status`, `fleet-status`, and `.freely/run/manager-worker-launch-state.env` agreed on the acceptance truth surface:
  - `latest_manager_continuity_generated == latest_manager_continuity_consumed == /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260324-034106.md`
  - `latest_manager_worker_prompts_generated == latest_manager_worker_prompts_consumed == /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260324-032208-worker-manager-active-worker-launch-state-reconcile-codex.txt`
  - `queued_worker_prompts = none`
  - `LAUNCHED_WORKER_PROMPTS` matched the same latest prompt path
  - `ACTIVE_RUNNING_WORKER_COUNT = 1` in that sampled patrol round, but this value is fleet-wide and not a lasting acceptance invariant for the issue family
- 2026-03-24 manager then generated the dedicated closeout continuity/prompt for this writeback lane, and the current canonical truth surfaces also show latest-truth consumption for that newer round:
  - `latest_manager_continuity_generated == latest_manager_continuity_consumed == /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/manager-continuity-20260324-051509.md`
  - `latest_manager_worker_prompts_generated == latest_manager_worker_prompts_consumed == /Users/zhaoyu/Downloads/code/my-freely/freely/.freely/run/worker-prompts/20260324-051509-worker-i-20260322-0445-closeout-codex.txt`
  - `queued_worker_prompts = none`
- 2026-03-24 follow-up patrol later saw `ACTIVE_RUNNING_WORKER_COUNT = 3` while unrelated worker lanes remained active in other issue families. That observation does not by itself reopen this issue because the fleet-wide worker count is not scoped to this issue family and the post-merge contract only requires same-round latest continuity / prompt consumption alignment.
- This confirms the issue family acceptance is closed on canonical `develop`: workers consumed the newest manager continuity / worker prompt truth instead of staying on an older delegated continuation, and active pending vs consumed delegated ids remained aligned.
- Cleanup is intentionally not executed from manager in this round. Keep the disposition explicit instead of pretending the lifecycle is retired:
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-launch-state-consumed-truth-reconcile`: retain until this docs-only closeout commit is absorbed by the develop-facing path; `merge-ready`, not `delete-ready`
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-active-worker-launch-state-reconcile`: retain; active same-family implementation lane still owns ongoing worker state
  - `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-pre-test-merge-lifecycle-management-followthrough`: retain as separate `runtime-owned` recovery lane after `secondary_rate_limit_exhausted`; do not fold it into this issue's acceptance result
- No further implementation or research scope remains inside `I-20260322-0445`. Any new regression after this closeout should reopen as a new continuation or new lifecycle based on the then-current truth source.

## Retirement Audit

- audit_date: `2026-03-24`
- worktree_path: `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-launch-state-consumed-truth-reconcile`
- worktree_state: `clean`
- classification: `retire-only`
- cleanup_gate: `retained-with-reason`
- why_not_verified_retirable:
  - current worktree still owns canonical closeout writeback for this issue family; writeback must be absorbed through the develop-facing path before branch/worktree cleanup
  - same-family worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-manager-active-worker-launch-state-reconcile` remains active and dirty, so this issue family is closed but not yet fully retired as a fleet unit
  - separate worktree `/Users/zhaoyu/Downloads/code/my-freely/freely-worktrees/20260324-feature-pre-test-merge-lifecycle-management-followthrough` remains `runtime-owned` recovery and must stay outside this issue's cleanup claim
- local_branch_disposition: `retained-with-reason`
- local_branch_reason: keep the branch/worktree until the docs-only closeout writeback is absorbed and supervisor/runtime runs the normal cleanup followthrough; do not delete from this worker round
- remote_branch_disposition: `not_checked`
- remote_branch_reason: remote cleanup is outside this worker's closeout-writeback scope
- revisit_trigger:
  - current docs-only closeout writeback is absorbed by the develop-facing path
  - supervisor/runtime re-enters cleanup followthrough for this worktree
