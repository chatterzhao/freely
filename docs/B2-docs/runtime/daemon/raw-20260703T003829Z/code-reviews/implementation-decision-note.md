---
issue_id: I-20260703T003829Z-A
issue_path: docs/B2-docs/runtime/daemon/raw-20260703T003829Z29Z/issues/I-20260703T003829Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260703T003829Z-A
- issue_path: docs/B2-docs/runtime/daemon/raw-20260703T003829Z29Z/issues/I-20260703T003829Z-A.md

## Implementation Decision Note

- decision: 用 `meta_env_value` 替换 `source "$state_file"` 读取 `LAST_ENTRYPOINT_MODE`
- why_this: `meta_env_value` 使用 `awk -F '"'` 安全提取值，不执行 shell 命令；是项目中已有的标准安全读取方式；改动最小（4 行 → 1 行）
- alternatives_considered: Option B（写入时 printf '%q' 转义）— 改动面大、跨平台不一致；Option C（grep+cut）— 引入新模式，与现有 meta_env_value 不一致
- boundary_non_goals: 不改 meta_env_value 本身；不改其他 source env 的调用点；不改 heredoc 写入格式
- residual_risk: 若未来有人绕过 write_workcell_state 直接写 workcell-state.env 且不用引号，meta_env_value 会返回空值（因为 awk 按 " 分割找不到第二个字段），进而 entrypoint_mode 为空，兜底为 "foreground"——不会执行命令，行为退化但安全
