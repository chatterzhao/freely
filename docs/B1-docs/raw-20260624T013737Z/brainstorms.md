# Brainstorms: tool-registry.json5 → TOML 配置驱动注册表

- raw_key: 20260624T013737Z
- github_issue: https://github.com/chatterzhao/freely/issues/3399

## Discovery

### 现状
8 个文件中有 ~28 处硬编码的 tool 特定逻辑（case 分支、if 判断、字段名常量）。
加新 AI CLI tool 需要修改所有这些文件。`tool-registry.json5` 定义了 3 个 tool 的基本字段但未被充分使用。

### 根因
没有统一的"工具接口描述"层。每个消费代码自己 hardcode tool 差异。

### 影响
- `tool-launchers.sh`: 启动语法、适配器检测 (~10 case)
- `session-cache.sh`: 会话目录/CLI 参数 (~7 case)
- `freely`: 恢复/边界/进程匹配 (~15 case)
- `monitor-ai-cli.sh`: 错误模式 (~3 case)
- `monitor-ai-acp.sh`: 权限读取 (~3 case)
- `acp-bridge.py`: ACP 二进制/权限 (~3 case)
- `deploy-skills`: 技能目录 (~3 case)
- `stream-json-bridge.py`: 二进制 (~1 case)

## Research

### 格式选择
- JSON5 → TOML: 用户熟悉（已有 config.toml、.codex/config.toml），Python 3.11+ 内置 tomllib
- 文件位置: ~/.freely/tool-registry.toml（用户） + <freely>/tool-registry.toml（系统）
- 合并: dict merge，用户覆盖系统同名 key

### 实施策略
10 阶段中，Phase 1（格式迁移）+ Phase 2（config_schema 驱动权限读取）是基础。后续 phase 可以渐进推进。

### 范围选择
**本次 PR 范围: Phase 1+2（基础层）**
- 创建 TOML 注册表文件（完整 schema，含所有 3 个 tool）
- 更新 tool-registry-query.py 支持 TOML + 双文件合并
- 添加 `_tool_config_field` 通用函数到 shared bash lib
- 用 config_schema.fields 消除 monitor-ai-acp.sh 和 tool-launchers.sh 中的权限字段硬编码
- 保留旧 JSON5 → 并行运行验证 → 后续 PR 删除

**延后到后续 PR**: Phase 3-10（session、launch、error_patterns 等）

## Decision

### 方案
Phase 1+2: TOML 格式 + 文件合并 + config_schema 权限字段抽象。
后续 PR 逐步迁移其余 case 分支。

### 理由
- 基础层必须先就位，其他 phase 依赖它
- config_schema 的"翻译层"设计验证了 registry 的核心价值
- 权限字段硬编码是最痛的点（monitor-ai-acp.sh 的 case 分支最复杂）

### 验收
1. tool-registry.toml 存在且包含完整 3 tool schema
2. `_tool_registry_get claude config_schema.fields.permission_bypass.path` → `permissionMode`
3. monitor-ai-acp.sh 的权限读取不再硬编码 permissionMode/approval_policy
4. `~/.freely/tool-registry.toml` 可覆盖系统内置
5. deploy-skills（已在 #3397 中改为 registry 驱动）继续工作
