# Issue: runtime-worker-launch-linkage-and-stall-recovery-governance

- issue_id: `I-20260322-0245`
- title: Runtime worker launch linkage and stall recovery governance
- phase_state: `in_verification`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `runtime-worker-launch-linkage-and-stall-recovery-governance`
- issue-name: `runtime-worker-launch-linkage-and-stall-recovery-governance`
- priority: P0
- source_candidate: `docs/pre-brainstorms/20260322-0245--runtime-worker-launch-linkage-and-stall-recovery/candidates.md#c-20260322-0245-a`
- source_brainstorm: `docs/pre-brainstorms/20260322-0245--runtime-worker-launch-linkage-and-stall-recovery/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/watchdog-live-status-surface-and-manager-supervision/issues/watchdog-live-status-surface-and-manager-supervision.md`
  - `docs/epics/workspace-routing-foundation/manager-delegation-after-sufficient-patrol-evidence-governance/issues/manager-delegation-after-sufficient-patrol-evidence-governance.md`
  - `docs/epics/workspace-routing-foundation/manager-continuation-handoff-consumption-governance/issues/manager-continuation-handoff-consumption-governance.md`

## Why

Freely 最新 dogfood 证明：

- manager 已能 patrol 并稳定产出 `retire-only / continue-dev`
- manager 已能写出 worker launch order 与 worker prompt artifact

但 runtime 还缺少两条关键能力：

1. 没有把这些 manager-generated worker handoff 转成目标 worker worktree 的实际执行
2. 长时间无输出且有待处理 intake 的 AI 进程不会被 runtime 识别成 stall 并恢复

因此 current gap 已经不在 manager prompt 语义，而在 runtime control plane。

## Scope

1. 定义 manager-generated worker handoff 的 runtime ingestion contract。
2. 将 manager worker handoff 转成 target worker worktree 的 delegated continuation / expected-running linkage，并实际触发 worker runtime。
3. 为当前 workcell 增加最小 stalled-AI detection 与 runtime-owned graceful recovery。
4. 补最小集成测试，验证：
   - manager handoff 会真正拉起 worker
   - stalled AI + pending intake 会触发 recovery

## Acceptance

- 主管写出 stable worker handoff 后，runtime 不再只停留在 `.freely/run/worker-prompts/*.txt`。
- target worker worktree 能收到可消费的 delegated continuation，并被 runtime 拉起。
- 当前 workcell AI 长时间无输出且存在更新的待处理 intake 时，runtime 能进行 graceful recovery；必要时落 hard-kill fallback evidence。
- 至少有一条 integration-style test 证明 manager handoff 能进入 worker execution。
- 至少有一条 runtime test 证明 stalled AI recovery 会让新 intake 进入下一轮 prompt。

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/runtime/manager-watchdog.sh`
- `docs/system/workspace/skills/watchdog-control-plane/SKILL.md`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/scripts/tests/test-*` for worker launch linkage and stalled recovery

## Verification

- `./bin/governance-check`
- worker launch linkage integration test
- stalled AI recovery runtime test
