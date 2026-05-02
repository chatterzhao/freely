# Issue: manager-chat-reentry-and-cleanup-misrouting-governance

- issue_id: `I-20260321-1925`
- title: Manager chat reentry and cleanup misrouting governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-chat-reentry-and-cleanup-misrouting-governance`
- issue-name: `manager-chat-reentry-and-cleanup-misrouting-governance`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/manager-chat-reentry-and-cleanup-misrouting-governance/code-reviews`
- source_candidate: `docs/pre-brainstorms/20260321-1925--manager-chat-reentry-and-cleanup-misrouting/candidates.md#c-20260321-1925-a`
- source_brainstorm: `docs/pre-brainstorms/20260321-1925--manager-chat-reentry-and-cleanup-misrouting/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/human-chat-intake-and-manager-delegation/issues/human-chat-intake-and-manager-delegation.md`, `docs/epics/workspace-routing-foundation/remote-branch-retirement-governance/issues/remote-branch-retirement-governance.md`
- session_refs:
  - {tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}

## Why

Freely 当前已经有：

- `chat -> intake -> interruption dispatcher`
- cleanup followthrough worker
- 主管巡检与 restart-point routing 的方法论真源

但真实集成测试显示：
- 当用户通过 chat 发起广义主管巡检任务时
- interruption manager triage 仍可能把它错误解释为 cleanup followthrough
- 结果是新的 supervisor-level signal 没回到 manager continuation，而是直接吸收到旧 cleanup continuity

## Scope

1. 收窄 interruption manager handler 的 cleanup 默认规则：
- 纯 cleanup / merged worktree retirement 仍走 `cleanup + worker`
- 广义主管巡检任务改走 `continuation + manager`

2. 保持边界：
- 不把广义主管巡检直接交给 manager 在 protected 工位施工
- 只让它回到 manager continuation / restart-point routing

3. 补回归：
- prompt-level regression
- runtime path regression

## Acceptance

- 广义主管巡检消息不再默认落到 `cleanup://merged-worktree-followthrough`
- 纯 cleanup 请求仍保持 cleanup 路径
- `test-interruption-manager-handler` 覆盖 supervisor-level chat case
- `test-freely-interruption-direct-answer` 覆盖 delegated continuation case

## Completion

- `docs/system/workspace/scripts/runtime/interruption-manager-handler`
- `docs/system/workspace/scripts/tests/test-interruption-manager-handler`
- `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- `docs/epics/workspace-routing-foundation/manager-chat-reentry-and-cleanup-misrouting-governance/code-reviews/20260321-manager-chat-reentry-and-cleanup-misrouting-verification.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-interruption-manager-handler`
- `bash docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`

## Next

- 当前批次已完成。
- 若后续又出现新的 manager-level chat signal 被旧 continuity 误吸收，应新开 lifecycle 承接，不在本 issue 上继续扩 scope。
