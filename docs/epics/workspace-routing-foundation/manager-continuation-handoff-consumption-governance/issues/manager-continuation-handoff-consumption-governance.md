# Issue: manager-continuation-handoff-consumption-governance

- issue_id: `I-20260322-0049`
- title: Manager continuation handoff consumption governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `manager-continuation-handoff-consumption-governance`
- issue-name: `manager-continuation-handoff-consumption-governance`
- verification_artifact_dir: `docs/epics/- epic-name: `workspace-routing-foundation`/- story-name: `manager-continuation-handoff-consumption-governance`/code-reviews`
- priority: P0
- source_candidate: `docs/pre-brainstorms/20260322-0049--manager-continuation-handoff-consumption/candidates.md#c-20260322-0049-a`
- source_brainstorm: `docs/pre-brainstorms/20260322-0049--manager-continuation-handoff-consumption/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on:
  - `docs/epics/workspace-routing-foundation/manager-chat-reentry-and-cleanup-misrouting-governance/issues/manager-chat-reentry-and-cleanup-misrouting-governance.md`
  - `docs/epics/workspace-routing-foundation/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md`
  - `docs/epics/workspace-routing-foundation/explicit-session-addressed-resume-governance/issues/explicit-session-addressed-resume-governance.md`
- session_refs:
  - {tool: codex, session_id: "019d147d-bff6-7e02-9cbd-133e8e9ebf2f", jsonl_path: "unavailable://manager-thread-jsonl-not-yet-traced", role: "manager-develop-runtime"}

## Why

Freely 当前已经具备：

- `chat -> intake -> interruption resolution`
- broad manager chat 不再误吸收到 cleanup followthrough
- local continuation re-entry 与 preemption evidence
- `fresh_with_handoff` 轮换与 continuity handoff

但真实 dogfood 证明：

- manager continuation handoff 已能生成
- handoff 也可能已经注入下一轮 prompt
- 但在 `context_compacted -> fresh_with_handoff -> auth_failure` 这类边界上，runtime 仍缺少明确的 generated-vs-consumed evidence
- 用户无法从 `live-status` 或 session state 直接判断：“这条 manager continuation handoff 是否已被主循环吃进去，还是仍然 pending / 被失败边界打断”

此外，`write_session_handoff()` 当前的 here-doc 里存在 shell-dangerous markdown backticks，已经在真实运行里触发过 `context: command not found`。

## Scope

1. 为 delegated manager continuation handoff 定义显式 evidence states：
   - generated
   - consumed_into_prompt
   - pending_after_failure
2. 让 runtime 在 prompt build / session rotation 中记录这些状态。
3. 把关键信息暴露到 `live-status` / baseline state。
4. 修复 `write_session_handoff()` 中会触发 shell command substitution 的 here-doc 内容。
5. 为 manager continuation consumption across `fresh_with_handoff` 补回归。

## Acceptance

- delegated manager continuation handoff 生成后，runtime 会记录 pending handoff ids
- 下一轮 prompt 若注入 delegated continuation，runtime 会记录 consumed handoff ids
- `live-status` 能显示 pending 与 last consumed manager continuation handoff
- `fresh_with_handoff` handoff 写入过程不再因 markdown backticks 触发 shell 命令替换
- regression test 覆盖：
  - delegated manager continuation 进入 prompt
  - pending/consumed evidence 写回
  - `fresh_with_handoff` handoff file generation shell-safe

## Completion

- `docs/system/workspace/scripts/runtime/freely`
- `docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- `docs/system/workspace/scripts/tests/test-freely-session-rotation`
- `docs/system/workspace/agents/manager-agent.md`
- `docs/system/workspace/skills/auto-loop-orchestrator/SKILL.md`
- `docs/progress/workspace-routing-foundation/p-manager-continuation-handoff-consumption-governance.md`
- `docs/epics/workspace-routing-foundation/manager-continuation-handoff-consumption-governance/code-reviews/20260322-manager-continuation-handoff-consumption-verification.md`

## Verification

- `./bin/governance-check`
- `bash docs/system/workspace/scripts/tests/test-freely-interruption-direct-answer`
- `bash docs/system/workspace/scripts/tests/test-freely-session-rotation`

## Next

- 当前批次已完成。
- cleanup followthrough 已确认当前 worktree 仅剩 `retire-only` 收口语义，且相关 anomaly 只保留 `historical-only` 追溯价值；不得因为这段历史事实重新打开本 issue 的 runtime/control-plane 实现范围。
- 若后续要继续扩“manager continuation 最终产出显式治理结论”的更高层语义，应通过新 lifecycle 承接，不在本 issue 上继续扩 scope。
