# ~/.ai-auth/ Slot 配置指南

## 什么是 Slot

Slot 是 AI CLI 工具的多账号/多 API key 隔离机制。每个 slot 是一个 `~/.ai-auth/` 下的目录，包含该工具的完整配置（API key、模型、权限等）。不同 slot 之间完全隔离，互不影响。

**为什么需要 Slot：**
- **多 API key 轮换**：一个 key 限流后切换到另一个
- **多账号隔离**：个人账号和工作账号分开
- **Freely 自动切换**：availability watchdog 检测到限流时自动切备用 slot

## ★ 命名约定（最重要）

Freely 运行时通过以下链式解析把 `config.toml` 的 `AI_TOOL` 值映射到 slot 配置：

```
config.toml        AI_TOOL = "claude-apikey-ds-flash-auto"
                        │
                        ▼  shell alias 解析
alias claude-apikey-ds-flash-auto="claude --settings ~/.ai-auth/claude-apikey-ds-flash-auto/settings.json ..."
                        │
                        ▼  _resolve_tool_family() 剥离 -apikey-* / -account-* 后缀
"claude"  ← 工具族
                        │
                        ▼  _apply_tool_alias_settings() 提取 env vars + --settings 路径
实际启动 claude，注入 ANTHROPIC_AUTH_TOKEN 等
```

**硬规则：slot 目录名 = `.zshrc` alias 名 = `config.toml` 的 `AI_TOOL` 值（三者完全一致）**

目录命名格式：`{tool}-{type}-{your-name}`

| 组件 | 说明 | 示例 |
|------|------|------|
| `{tool}` | `claude` / `codex` / `opencode` | Freely 据此识别工具族 |
| `{type}` | `apikey`（API key 模式）/ `account`（OAuth 模式） | `-apikey-` / `-account-` 前缀是硬依赖 |
| `{your-name}` | 自定义，描述 provider/账号/用途 | `ds-flash-auto`、`my-openai` |

**改名时三处同步改**：目录名 → alias 名 → `AI_TOOL` 值。任何一处不一致都会导致运行时找不到 slot。

## 三种工具对比

| | Claude Code | Codex | OpenCode |
|---|---|---|---|
| **目录** | `claude-apikey-{name}/` | `codex-account-{name}/` | `opencode-apikey-{name}/` |
| **配置** | `settings.json` | 完整 CODEX_HOME | `settings.json` |
| **model** | ✅ 在 settings.json | ✅ 在 config.toml | ✅ 在 settings.json |
| **API key** | ✅ 在 settings.json `env` 中 | ✅ `auth.json`（需 login 生成） | ❌ 不在 settings.json 内（需 env var） |
| **permissions** | ✅ `permissionMode` + `permissions.deny` | ✅ `approval_policy` + `sandbox_mode` | ✅ `permission` |
| **别名** | `claude --settings ...` | `CODEX_HOME=... codex` | `OPENCODE_CONFIG=... opencode` |

## 快速开始

### 1. 建 slot 目录

```bash
# Claude Code（API key 模式）
mkdir -p ~/.ai-auth/claude-apikey-my-provider

# Codex（OAuth 模式）
mkdir -p ~/.ai-auth/codex-account-my-openai

# OpenCode（API key 模式）
mkdir -p ~/.ai-auth/opencode-apikey-my-provider
```

### 2. 复制模板并填入真实值

```bash
# 模板位置：<freely-project>/.freely/ai-auth/
# 或：<freely-project>/templates/ai-auth/

cp .freely/ai-auth/claude-apikey-EXAMPLE/settings.json.example \
   ~/.ai-auth/claude-apikey-my-provider/settings.json
# → 编辑 settings.json，把 your-apikey 替换为真实 key
```

### 3. 加 alias 到 ~/.zshrc

参考 `.freely/ai-auth/zshrc-aliases.example`，追加到 `~/.zshrc` 尾部：

```bash
# Claude Code
alias claude-apikey-my-provider="claude --settings $HOME/.ai-auth/claude-apikey-my-provider/settings.json --dangerously-skip-permissions"

# OpenCode（注意 API key 需单独设置）
export DEEPSEEK_API_KEY="your-apikey"
alias opencode-apikey-my-provider='OPENCODE_CONFIG="$HOME/.ai-auth/opencode-apikey-my-provider/settings.json" opencode'

# Codex
alias codex-account-my-openai='CODEX_HOME="$HOME/.ai-auth/codex-account-my-openai" codex'
```

### 4. 设 AI_TOOL

在 `.freely/config.toml` 中：

```toml
AI_TOOL = "claude-apikey-my-provider"
```

### 5. 验证

```bash
source ~/.zshrc
claude-apikey-my-provider -p "say hi"
# 应正常返回 "hi"
```

## Slot 切换

- **手动切换**：修改 `.freely/config.toml` 的 `AI_TOOL` 值，重启 Freely daemon
- **自动切换**：availability watchdog 检测到当前 slot 限流时自动换备用 slot（需配置 `AUTO_SWITCH_SLOT = true`）

## 安全注意事项

1. **权限隔离**：
   ```bash
   chmod 700 ~/.ai-auth
   chmod 600 ~/.ai-auth/*/settings.json
   chmod 600 ~/.ai-auth/*/auth.json
   ```

2. **不要提交到 Git**：`~/.ai-auth/` 在 home 目录下，不在任何仓库中

3. **占位符检查**：确认所有 `your-apikey` 都已替换为真实值

4. **不要共享**：settings.json / auth.json 等同于你的账号凭证，不要分享给任何人
