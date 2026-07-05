# Issue: worker-active-reentry-for-manager-delegated-continuation-governance

- issue_id: `I-20260322-0412`
- title: Worker active reentry for manager-delegated continuation governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `worker-active-reentry-for-manager-delegated-continuation-governance`
- issue-name: `worker-active-reentry-for-manager-delegated-continuation-governance`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/worker-active-reentry-for-manager-delegated-continuation-governance/code-reviews`
- priority: P0
- source_candidate: `docs/B1-docs/raw-20260322/candidates.md#c-20260322-0412-a`
- source_brainstorm: `docs/B1-docs/raw-20260322/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/runtime-worker-launch-linkage-and-stall-recovery-governance/issues/runtime-worker-launch-linkage-and-stall-recovery-governance.md`

## Why

manager runtime 已经能把 stable worker prompt 转成目标 worker worktree 的 delegated continuation intake，并拉起 worker runtime。但当目标 worker 已经有 active AI 时，这条 delegated continuation 不会被及时消费，导致“worker 已活着，但 handoff 没真正进入下一轮”。

## Scope

1. 明确 manager runtime 写入 worker intake 后的 active-worker handling contract。
2. 若目标 worker 已 active：
   - 不再只写 intake；
   - 显式触发 local continuation reentry；
   - 不额外再起第二个 worker supervisor。
3. 补脚本级测试，覆盖 active worker + manager launch handoff 的真实路径。
4. 写回 watchdog/runtime 真源，说明这是 `runtime-owned` reentry，不是 manager/worker 自行决定。

## Acceptance

- manager runtime 处理 worker prompt 时，若目标 worker 已有 active AI：
  - 会触发 `request_local_continuation_reentry(target, intake_id)`；
  - 不会再额外重复起一个 supervisor。
- 目标 worker 的 delegated continuation 进入下一轮 prompt / consumed evidence，不再长期悬空。
- 现有 manager->worker launch linkage 测试不回退。

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- `docs/system/workspace/scripts/tests/test-freely-manager-worker-launch-linkage`
- `docs/system/workspace/scripts/tests/test-freely-worker-active-reentry-from-manager-launch`
- `docs/progress/workspace-routing-foundation/p-worker-active-reentry-for-manager-delegated-continuation-governance.md`
- `docs/epics/workspace-routing-foundation/worker-active-reentry-for-manager-delegated-continuation-governance/code-reviews/20260322-worker-active-reentry-for-manager-delegated-continuation-verification.md`

## Verification Summary

- 脚本级验收已覆盖：
  - inactive worker 仍按原路径被拉起；
  - active worker 会触发 `request_local_continuation_reentry`，而不是重复启动第二个 supervisor。
- merge 后在 `develop` 做了真实 runtime acceptance：
  - manager runtime 生成新的 worker prompt / manager continuity；
  - 对已 active 的 `feature/cli-first-observability-surfaces-20260322` 触发了真实 `graceful_term`；
  - worker 写出了 `LAST_PREEMPTION_REASON="local_continuation_reentry"`；
  - worker 随后拉起了新的 AI 进程，且 `current_prompt_has_delegated_continuation: 1`。
- 观察到 `last_consumed_delegated_continuation_ids` 仍按 cycle completion 回写，属于既有 consumption evidence 节奏，不阻塞本次 active-worker reentry 修复收口。
