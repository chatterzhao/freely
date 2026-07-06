# Tasks: tool-registry TOML 配置驱动（Phase 1+2）
- issue_id: I-20260624T013737Z-A

## Phase 1: TOML 格式迁移
### T1: 创建 tool-registry.toml
- 新建 `tool-registry.toml`，包含 claude/codex/opencode 完整 schema
- status: pending

### T2: 更新 tool-registry-query.py
- 支持 TOML 读取（tomllib）+ 双文件合并（~/.freely 优先）
- status: pending

## Phase 2: config_schema 字段抽象
### T3: monitor-ai-acp.sh 权限字段
- case 分支 → config_schema.fields.permission_bypass 查询
- status: pending

### T4: tool-launchers.sh 权限字段
- `_apply_tool_alias_settings` 硬编码 → registry 驱动
- status: pending

### T5: freely _bridge_env_for_registered_tool
- 补充完整 config_schema 抽象
- status: pending

### T6: 手动测试验证
- daemon start + deploy-skills --dry-run + permission 读取
- status: pending
