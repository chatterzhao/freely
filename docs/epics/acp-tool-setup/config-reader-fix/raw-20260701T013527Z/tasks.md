# Tasks: get_config 修复

- issue_id: I-20260701T013527Z-A

## Task 1: 应用修复
- [ ] 将 `docs/system/workspace/scripts/runtime/freely` L14052 的 `get_config "$_config_key" ""` 替换为 `${!_config_key:-}`
- 改动: 1 行
- 风险: 极低

## Task 2: 验证
- [ ] 启动 daemon 确认无 `get_config: command not found` 错误
- [ ] 确认 daemon 正常启动
