# Pre-Tests: session-lifecycle-rotation-and-handoff-governance

1. 首轮启动使用 `fresh`。
2. 正常短会话在未命中 rotation 条件时继续 `resume`。
3. 若最近 cycle log 包含 `context compacted`，下一轮改走 `fresh_with_handoff`。
4. 第二轮 fresh prompt 中能看到 handoff 交接内容。
5. 若项目未显式指定 Codex model / reasoning effort，runtime 仍写入 `gpt-5.4` 与 `medium`。
