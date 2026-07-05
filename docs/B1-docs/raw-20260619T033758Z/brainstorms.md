# Brainstorm: login claude 缺少交互式 slot 命名与 alias 创建

## discovery

- **来源**: `raw-20260619T033758Z` — `freely feedback` 创建，触发于开发过程中发现 `freely ai login claude` 行为不符合预期
- **时效性**: 新鲜 issue（2026-06-19），核心命令交互缺陷，当前项目阶段高度相关
- **覆盖检查**: 未被其他 issue/candidate 覆盖；这是 `ai-cli` 脚本中非 codex 工具登录路径的独立缺陷

## research

### 现状分析

`freely ai login claude` 的完整调用链最终落在 `tool_login_generic`，该函数：
1. 无任何交互提示（不询问 auth_mode、不询问 slot name）
2. 硬编码生成 `claude-default-1` 作为 slot 名
3. 只创建空目录，不写 `settings.json` 配置模板
4. 不创建 shell alias

对比 `login codex`（L1200-1254：~55 行完整登录+保存+alias 逻辑），claude 分支只有一行 `tool_login_generic "$tool"`。

### 根因

`tool_login_generic` 设计意图是"轻量容器创建"（适合 iflow 这种 auth 来自环境变量、slot 仅调度器兼容的场景），被错误地复用到 claude/opencode/cc/kiro-cli 等需要完整交互式配置+alias 的工具。

### 边界约束

- **CONSTITUTION.md**: 无冲突。修改限于单个脚本文件，不涉及架构变更。
- **LAWS.md**: 无违反。此修复不触及保护分支、门禁或治理边界。
- **PROJECT_INTENT.md**: 对齐。改善 AI CLI 工具的用户体验，符合"自主开发工具链"的意图。

### 依赖

- 无外部依赖。修改完全自包含在 `docs/system/workspace/scripts/runtime/ai-cli`。
- 不依赖其他未合并分支或 milestone。

## decision

### 方案选择

采用参照 `login codex` 的两步交互模式：

```
freely ai login claude
  → 1. 提示 auth_mode (account/apikey)
       ├─ apikey → 提示 slot name → 创建 settings.json + alias
       └─ account → 提示 slot name → 创建目录 + alias
```

具体改动：

| # | 改动 | 说明 |
|---|------|------|
| 1 | 新增 `_prompt_generic_login_mode` | 为 claude/opencode/cc/kiro-cli 提供 account/apikey 交互选择 |
| 2 | 新增 `_login_account_slot` | account 模式 slot 创建：提示名称→创建目录→添加 alias |
| 3 | 修改 `cmd_login` claude 分支 | 替换 `tool_login_generic`，增加交互路由 |
| 4 | 修改 `_login_apikey_alias` | `--name` 为空时交互提示，空输入终止 |
| 5 | 更新 settings.json 骨架 | 从 3 行简陋模板→Anthropic 完整骨架 |

### 推荐下一跳

**直接 promote**。问题边界清晰，实现已完成且通过测试（6 个场景全部验证通过），无需继续 research。转入 `freely-doc-B2_IBM-execution` 产出 I-issue。
