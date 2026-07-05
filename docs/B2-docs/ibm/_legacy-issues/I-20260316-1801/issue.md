---
local_id: I-20260316-1801
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '9'
    url: https://github.com/chatterzhao/freely/issues/9
    synced_at: '2026-04-27T11:12:27Z'
  gitee:
    issue_id: IJFO4V
    url: https://gitee.com/zhaoquan/freely/issues/IJFO4V
    synced_at: '2026-04-27T13:13:49Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/session-lifecycle-rotation-and-handoff-governance/issues/session-lifecycle-rotation-and-handoff-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:12:27Z'
hash: ''
created_at: '2026-04-27T11:12:27Z'
updated_at: '2026-04-27T11:12:27Z'
platform_state: closed
---

# Issue: session-lifecycle-rotation-and-handoff-governance

- issue_id: `I-20260316-1801`
- title: Auto-run session lifecycle rotation and handoff governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `session-lifecycle-rotation-and-handoff-governance`
- issue-name: `session-lifecycle-rotation-and-handoff-governance`
- verification_artifact_dir: `docs/epics/workspace-routing-foundation/session-lifecycle-rotation-and-handoff-governance/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260303/candidates.md#c-20260303-103`
- source_brainstorm: `docs/B1-docs/raw-20260303/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/epics/workspace-routing-foundation/business-block-vs-system-crash-recovery/issues/business-block-vs-system-crash-recovery.md`
- session_refs: [{tool: codex, session_id: "current-thread", jsonl_path: "unavailable://codex-thread-only", role: "author"}]

## Why

Freely 需要明确区分：

- “当前工具会话还能 resume”
- “继续 resume 仍然是最优策略”

如果 runtime 没有 session rotation 与 handoff 机制，后台狗粮运行就会在 `context compacted` 后继续盲目 resume 同一会话，导致首跳反复重做、结论重复输出、fresh session 也没有最小交接面。

## Scope

1. 为 auto-run AI CLI 增加 `fresh_with_handoff` 轮换语义。
2. 定义 session rotation 的最小触发条件。
3. 记录 session state，使 supervisor 能依据上一轮输出决定下一轮是 `resume` 还是 `fresh`。
4. 生成最小 handoff 文件并拼接进下一轮首跳 prompt。
5. 明确 Codex 默认运行配置继续固定为 `gpt-5.4 + medium`。
6. 增加脚本级回归测试，锁住 `context compacted -> fresh_with_handoff` 行为。
7. 对 Codex 增加基于 `token_count / model_context_window` 的 context-window-aware warn / rotate 策略。

## Acceptance

- Runtime 不再“一律在首轮后 resume”。
- 当最近一轮输出出现 `context compacted` 时，下一轮切到 `fresh_with_handoff`。
- 当最近一轮上下文占用达到本地 rotate 阈值时，下一轮切到 `fresh_with_handoff`。
- 当最近一轮上下文占用达到本地 warn 阈值但未到 rotate 阈值时，下一轮 prompt 先提醒更新 continuity artifact。
- Runtime 能记录 `previous_tool_session_id`、`previous_cycle_
