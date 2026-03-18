# Profile 配置规范

本文档定义 Freely 管理 AI CLI profile 的配置格式和规范。

## 配置文件位置

全局配置文件：`~/.config/freely/ai-cli-profiles.yaml`

## 快速配置（推荐）

```bash
# 1. 登录 codex 账号1
codex login
# 完成后保存为 personal profile
freely ai-cli save codex personal

# 2. 登录 codex 账号2
codex login
# 完成后保存为 work profile
freely ai-cli save codex work

# 3. 查看已保存的 profile
freely ai-cli list
```

**原理**：`freely ai-cli save` 自动复制当前 `~/.codex/auth.json` 到 `~/.ai-auth/codex-<profile>/`

## 目录结构

```
~/.ai-auth/                    # 授权文件目录（自动管理）
├── codex-personal/auth.json
├── codex-work/auth.json
└── codex-backup/auth.json

~/.config/freely/
└── ai-cli-profiles.yaml       # 配置文件（自动生成）
```

## 配置格式

```yaml
version: 1
default_tool: codex

tools:
  codex:
    method: copy_auth
    active: personal
    profiles:
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
    profiles:
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
| `freely ai-cli save <tool> <profile>` | 保存当前登录账号为 profile |
| `freely ai-cli switch <tool> <profile>` | 切换到指定 profile |
| `freely ai-cli list` | 列出所有 profile |
| `freely ai-cli status` | 查看当前状态 |
| `freely ai-cli delete <tool> <profile>` | 删除指定 profile |

## save 命令实现

```bash
freely_ai_cli_save() {
  local tool="$1"
  local profile="$2"
  
  case "$tool" in
    codex)
      # 检查当前登录
      [ -f ~/.codex/auth.json ] || { echo "错误: 请先 codex login"; exit 1; }
      
      # 创建目录并复制
      mkdir -p ~/.ai-auth/codex-$profile
      cp ~/.codex/auth.json ~/.ai-auth/codex-$profile/
      chmod 600 ~/.ai-auth/codex-$profile/auth.json
      
      # 更新配置文件
      update_profiles_config codex "$profile"
      
      echo "已保存 codex profile: $profile"
      ;;
    iflow)
      echo "iflow 使用环境变量，请在 ~/.zshrc 中设置 IFLOW_${profile}_KEY"
      ;;
  esac
}
```

## 切换流程

```bash
freely_ai_cli_switch() {
  local tool="$1"
  local profile="$2"
  local auth_dir=~/.ai-auth/codex-$profile
  
  # 检查 profile 是否存在
  [ -d "$auth_dir" ] || { echo "错误: profile $profile 不存在"; exit 1; }
  
  # 备份当前授权
  [ -f ~/.codex/auth.json ] && cp ~/.codex/auth.json ~/.codex/auth.json.bak
  
  # 复制新授权
  cp "$auth_dir/auth.json" ~/.codex/auth.json
  
  # 更新活跃 profile
  update_active_profile codex "$profile"
  
  echo "已切换到 codex profile: $profile"
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
