# Issue: session-lifecycle-rotation-and-handoff-governance

- issue_id: `I-20260316-1801`
- title: Auto-run session lifecycle rotation and handoff governance
- phase_state: `completed`
- milestone: `M-20260306-workspace-routing-foundation`
- epic-name: `workspace-routing-foundation`
- story-name: `session-lifecycle-rotation-and-handoff-governance`
- issue-name: `session-lifecycle-rotation-and-handoff-governance`
- verification_artifact_dir: `docs/B2-docs/ibm/session-lifecycle-rotation-and-handoff-governance/code-reviews`
- source_candidate: `docs/B1-docs/raw-20260303/candidates.md#c-20260303-103`
- source_brainstorm: `docs/B1-docs/raw-20260303/brainstorms.md`
- execution_base: `develop`
- integration_target: `develop`
- depends_on: `docs/B2-docs/runtime/business-block-vs-system-crash-recovery/issues/business-block-vs-system-crash-recovery.md`
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
- Runtime 能记录 `previous_tool_session_id`、`previous_cycle_log`、`resume_streak` 与 `rotation_reason`。
- Runtime 能记录 `previous_tool_jsonl_path` 与 `context_ratio`。
- Fresh handoff 会拼接到下一轮 prompt，而不是丢失上一轮上下文。
- Codex 默认启动配置为 `gpt-5.4` 与 `medium`，除非项目显式覆盖。
- 脚本级测试能证明 compaction 后不会继续盲目 resume。

## Completion

- `docs/system/workspace/scripts/runtime/freely` 已支持：
  - Codex 默认模型 `gpt-5.4`
  - Codex 默认 reasoning effort `medium`
  - session state 记录
  - `context compacted` 与 resume streak 的 session rotation
  - handoff 文件生成与 prompt 注入
- `docs/system/workspace/scripts/monitor-ai-cli.sh` 已补 `test-compact` 测试模拟器。
- `docs/system/workspace/scripts/tests/test-freely-session-rotation` 已覆盖 `context compacted -> fresh_with_handoff`。
- `docs/LAWS.md` 已补上“可 resume 不等于必须继续 resume”与 `fresh_with_handoff` 最小交接面的治理说明。
- 当前扩展继续把 Codex `jsonl_path / context_ratio` 纳入 runtime 容量治理，用于在 compact 之前做 continuity 提醒与轮换。
