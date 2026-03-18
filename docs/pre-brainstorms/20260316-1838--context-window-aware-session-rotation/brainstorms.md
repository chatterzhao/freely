# Brainstorms: context-window-aware-session-rotation

## Why

Freely 已经支持基于 `context compacted`、缺失 resume 证据和 resume streak 的 `fresh_with_handoff`。但对于 Codex 这类会持续输出 `token_count` / `model_context_window` 的工具，runtime 仍然只能在“已经 compact 之后”被动轮换，缺少更早的上下文容量治理。

这会让 Freely 自举开发自己时出现两个问题：

1. 会话在上下文压力已经明显升高时仍盲目继续延长。
2. continuity 更新没有被作为显式的生命周期动作前置到轮换前，而是等到 compact 或人工介入后再补。

## Convergence

1. 对 Codex 运行时增加 context-window-aware 策略：
   - `warn` 阈值：当最近一轮上下文占用比例达到阈值时，下一轮继续前先提醒 AI 更新阶段连续性产物。
   - `rotate` 阈值：当最近一轮上下文占用比例达到更高阈值时，下一轮直接走 `fresh_with_handoff`。
2. continuity 更新目标必须按 loop 分层：
   - `dev-loop`：优先 `docs/progress/**`，未启用时退回规范允许的等价留痕
   - `doc-loop`：更新当前 issue / IBM / pre-brainstorm 产物
   - `recovery`：更新 recovery 或 progress/recovery 等价落点
3. runtime 自己不直接伪造业务文档路径，但必须把“当前需要先更新 continuity artifact”写入 prompt / handoff。
4. Codex session evidence 除 `session_id` 外，还应补出 `jsonl_path` 和最近的 `context_ratio`，供 status / recovery / handoff 使用。

## Decision

- 使用双阈值，而不是“到 50% 就强制 fresh”：
  - `warn`: `0.50`
  - `rotate`: `0.70`
- `warn` 只触发 continuity-update 提醒，不切会话。
- `rotate` 触发 `fresh_with_handoff`，并在交接中明确写出：
  - `previous_tool_session_id`
  - `previous_tool_jsonl_path`
  - `context_ratio`
  - `summary_target_hint`
  - 最近输出摘录
- 该能力属于现有 session lifecycle story 的扩展，不需要新开并行 runtime story；但必须先在 pre-brainstorm 留痕，再进入实现。
