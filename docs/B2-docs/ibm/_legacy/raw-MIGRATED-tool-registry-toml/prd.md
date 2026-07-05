# PRD: tool-registry TOML 配置驱动注册表（Phase 1+2）

## Goal
将 `tool-registry.json5` 升级为 TOML 格式的完整配置驱动注册表，为消除全部 ~28 处硬编码建立基础设施。Phase 1+2 建立基础层：TOML 格式 + 文件合并优先级 + config_schema 权限字段抽象。

## Dev-Loop Handoff
1. 创建 `tool-registry.toml`（当前 JSON5 的 TOML 对等物 + 完整 schema）
2. 更新 `tool-registry-query.py` 支持 TOML + 合并逻辑
3. 重构 `monitor-ai-acp.sh` 权限读取路径
4. 重构 `tool-launchers.sh` 权限字段读取
5. 重构 `freely` `_bridge_env_for_registered_tool` 补充完整抽象

## Non-Goals
- 不迁移 Phase 3-10 的 session/launch/error_patterns 等 case 分支
- 不删除旧 JSON5 文件（并行运行验证）
- 不改变 tool 行为的逻辑，只改变字段读取方式
