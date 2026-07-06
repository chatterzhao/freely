# Tasks: session-lifecycle-rotation-and-handoff-governance

- 为 runtime 增加 session state 文件与 handoff 文件。
- 定义 `context compacted` 与 resume streak 的 rotation 触发条件。
- 把 handoff 拼接进下一轮首跳 prompt。
- 固定 Codex 默认运行配置为 `gpt-5.4 + medium`。
- 增加脚本级回归测试。
