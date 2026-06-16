# 授权文件准备与验证

> **Slot 配置模板**：`templates/ai-auth/codex-account-EXAMPLE/config.toml.example`
> 提供了完整的 Codex slot 配置模板。按 `templates/ai-auth/README.md` 操作。
>
> ★ **命名约定**：slot 目录名 = `.zshrc` alias 名 = `config.toml` `AI_TOOL` 值，
> 三者必须一致。Codex slot 格式为 `codex-account-{your-name}`。

## codex 授权文件

### 强制文件存储

在 `~/.codex/config.toml` 中设置：

```toml
cli_auth_credentials_store = "file"
```

这确保授权保存在 `auth.json` 文件而非系统 keyring，便于复制迁移。

### 登录并导出

```bash
# 1. 登录账号
codex login

# 2. 确认文件生成
ls -l ~/.codex/auth.json

# 3. 复制到统一授权目录
mkdir -p ~/.ai-auth/codex-personal
cp ~/.codex/auth.json ~/.ai-auth/codex-personal/

# 4. 设置权限
chmod 600 ~/.ai-auth/codex-personal/auth.json
```

### 验证登录

```bash
codex --version
codex  # 应直接进入 TUI 无登录提示
```

### 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| auth.json 不存在 | 使用 keyring 存储 | 设置 `cli_auth_credentials_store = "file"` 后重新登录 |
| 登录失败 | config.toml 冲突 | 检查 `forced_login_method` 或 workspace 限制 |
| 权限错误 | 文件权限问题 | `chmod 600 ~/.codex/auth.json` |

## iflow 授权配置

iflow 使用环境变量或 `settings.json`，无需文件迁移：

```bash
# 方式 1：环境变量
export IFLOW_apiKey="sk-xxxxx"

# 方式 2：settings.json
# ~/.iflow/settings.json 中设置 apiKey
```

## 安全注意事项

1. **auth.json = 访问令牌**：切勿提交到仓库或在聊天中公开
2. **权限隔离**：`chmod 700 ~/.ai-auth` 和 `chmod 600` 授权文件
3. **备份**：切换前自动备份当前授权
4. **不读取内容**：Freely 仅复制文件，不解析内容

## 批量准备脚本

```bash
#!/bin/bash
# prepare-codex-auth.sh

AUTH_DIR="$HOME/.ai-auth"

# 创建目录结构
mkdir -p "$AUTH_DIR"/{codex-personal,codex-work,codex-backup}
chmod 700 "$AUTH_DIR"

# 确保使用文件存储
grep -q "cli_auth_credentials_store" ~/.codex/config.toml || \
  echo 'cli_auth_credentials_store = "file"' >> ~/.codex/config.toml

echo "准备完成。请依次登录各账号并运行："
echo "  cp ~/.codex/auth.json $AUTH_DIR/codex-personal/"
echo "  cp ~/.codex/auth.json $AUTH_DIR/codex-work/"
```
