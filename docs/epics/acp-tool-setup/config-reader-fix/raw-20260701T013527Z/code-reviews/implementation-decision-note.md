---
issue_id: I-20260701T013527Z-A
issue_path: docs/epics/acp-tool-setup/config-reader-fix/raw-20260701T013527Z/issues/I-20260701T013527Z-A.md
phase_state: done_b2_ibm
---

- issue_id: I-20260701T013527Z-A
- issue_path: docs/epics/acp-tool-setup/config-reader-fix/raw-20260701T013527Z/issues/I-20260701T013527Z-A.md

## Implementation Decision Note

- decision: 将 L14052 的 `get_config "$_config_key" ""` 替换为 `${!_config_key:-}`
- why_this: load_config 已通过 toml2env 导出所有配置值为环境变量，bash indirect expansion 直接读取，零 IO、无新函数
- alternatives_considered:
  - 定义 get_config 函数：需重复解析 config.toml，增加维护负担
  - 使用 _read_config_value (L20161)：嵌套函数不在当前作用域，依赖 Python 子进程
- boundary_non_goals: 不改动其他任何代码，不引入新函数
- residual_risk: 无。若 config.toml 中该 key 不存在，`_config_path` 为空字符串，后续逻辑保持不变（回退到 PATH 搜索）
