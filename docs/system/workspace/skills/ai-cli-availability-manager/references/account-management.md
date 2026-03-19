# Account 配置规范

本文档定义 Freely 管理 AI CLI account 的配置格式和规范。

## 配置文件位置

全局配置文件：`~/.config/freely/ai-cli-accounts.yaml`

## 快速配置（推荐）

```bash
# 1. 登录 codex 账号1
codex login
# 完成后保存为 personal account
freely ai-cli save codex personal

# 2. 登录 codex 账号2
codex login
# 完成后保存为 work account
freely ai-cli save codex work

# 3. 查看已保存的 account
freely ai-cli list
```

**原理**：`freely ai-cli save` 自动复制当前 `~/.codex/auth.json` 到 `~/.ai-auth/codex-<account>/`

## 目录结构

```
~/.ai-auth/                    # 授权文件目录（自动管理）
├── codex-personal/auth.json
├── codex-work/auth.json
└── codex-backup/auth.json

~/.config/freely/
└── ai-cli-accounts.yaml       # 配置文件（自动生成）
```

## 配置格式

```yaml
version: 1
default_tool: codex

tools:
  codex:
    method: copy_auth
    active: personal
    accounts:
      personal:
        auth_dir: ~/.ai-auth/codex-personal
        description: 个人账号
      work:
        auth_dir: ~/.ai-auth/codex-work
        description: 工作账号
    strategy:
      mode: round-robin
      skip_cooling: true
  
  iflow:
    method: env_var
    active: default
    accounts:
      default:
        env:
          IFLOW_apiKey: $IFLOW_DEFAULT_KEY

state:
  codex:
    personal:
      last_used: 2026-03-18T10:30:00Z
      status: active
```

## CLI 命令

| 命令 | 说明 |
|------|------|
| `freely ai-cli save <tool> <account>` | 保存当前登录账号为 account |
| `freely ai-cli switch <tool> <account>` | 切换到指定 account |
| `freely ai-cli list` | 列出所有 account |
| `freely ai-cli status` | 查看当前状态 |
| `freely ai-cli delete <tool> <account>` | 删除指定 account |

## save 命令实现

```bash
freely_ai_cli_save() {
  local tool="$1"
  local account="$2"
  
  case "$tool" in
    codex)
      # 检查当前登录
      [ -f ~/.codex/auth.json ] || { echo "错误: 请先 codex login"; exit 1; }
      
      # 创建目录并复制
      mkdir -p ~/.ai-auth/codex-$account
      cp ~/.codex/auth.json ~/.ai-auth/codex-$account/
      chmod 600 ~/.ai-auth/codex-$account/auth.json
      
      # 更新配置文件
      update_accounts_config codex "$account"
      
      echo "已保存 codex account: $account"
      ;;
    iflow)
      echo "iflow 使用环境变量，请在 ~/.zshrc 中设置 IFLOW_${account}_KEY"
      ;;
  esac
}
```

## 切换流程

```bash
freely_ai_cli_switch() {
  local tool="$1"
  local account="$2"
  local auth_dir=~/.ai-auth/codex-$account
  
  # 检查 account 是否存在
  [ -d "$auth_dir" ] || { echo "错误: account $account 不存在"; exit 1; }
  
  # 备份当前授权
  [ -f ~/.codex/auth.json ] && cp ~/.codex/auth.json ~/.codex/auth.json.bak
  
  # 复制新授权
  cp "$auth_dir/auth.json" ~/.codex/auth.json
  
  # 更新活跃 account
  update_active_account codex "$account"
  
  echo "已切换到 codex account: $account"
  echo "请重启 codex 使授权生效"
}
```

## 首次使用流程

```bash
# 1. 准备环境
freely ai-cli init

# 2. 依次登录并保存各账号
codex login && freely ai-cli save codex personal
codex login && freely ai-cli save codex work
codex login && freely ai-cli save codex backup

# 3. 验证
freely ai-cli list
```

## 安全

- `~/.ai-auth/` 权限自动设为 `700`
- 授权文件权限自动设为 `600`
- Freely 不读取授权文件内容，仅复制
