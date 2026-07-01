# PRD: 修复 get_config 未定义

## Goal
修复 `docs/system/workspace/scripts/runtime/freely` 第 14052 行调用未定义函数 `get_config` 的 bug。

## Scope
- 单行修复：L14052 `get_config "$_config_key" ""` → `${!_config_key:-}`
- 无其他文件改动
- 无 API 变更
- 无配置格式变更

## Dev-Loop Handoff
- RED: 通过 grep 确认 `get_config` 未定义，启动 daemon 观察错误日志
- dev: 应用单行修复
- GREEN: 启动 daemon 确认不再报错
