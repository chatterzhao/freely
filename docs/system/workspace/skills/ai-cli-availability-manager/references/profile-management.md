# Profile 配置规范

本文档定义 Freely 管理 AI CLI profile 的配置格式和规范。

## 配置文件位置

全局配置文件：`~/.config/freely/ai-cli-profiles.yaml`

项目级覆盖（可选）：`<project>/.env/ai-cli-profiles.yaml`

## 配置格式

```yaml
# AI CLI Profile 配置
version: 1

# 默认工具（可选，启动时可覆盖）
default_tool: codex

# 各工具的 profile 配置
tools:
  codex:
    # 切换方式：copy_auth（复制授权文件）或 env_var（环境变量切换目录）
    method: copy_auth
    
    # 当前活跃 profile
    active: personal
    
    # profile 定义
    profiles:
      personal:
        # 授权文件路径（method=copy_auth 时使用）
        auth_file: ~/.codex-profiles/personal/auth.json
        # 配置文件路径（可选，如需要切换不同配置）
        config_file: ~/.codex-profiles/personal/config.toml
        description: 个人账号
        tags: [personal, primary]
        
      work:
        auth_file: ~/.codex-profiles/work/auth.json
        config_file: ~/.codex-profiles/work/config.toml
        description: 工作账号
        tags: [work]
        
      backup:
        auth_file: ~/.codex-profiles/backup/auth.json
        description: 备用账号
        tags: [backup]
    
    # profile 选择策略
    strategy:
      mode: round-robin  # round-robin, random, priority
      skip_cooling: true
  
  iflow:
    # iflow 使用环境变量覆盖（会话位置固定，不影响连续性）
    method: env_var
    active: default
    profiles:
      default:
        env:
          IFLOW_apiKey: $IFLOW_DEFAULT_KEY
          IFLOW_baseUrl: https://apis.iflow.cn/v1
        description: 默认账号
        
      backup:
        env:
          IFLOW_apiKey: $IFLOW_BACKUP_KEY
          IFLOW_baseUrl: https://apis.iflow.cn/v1
        description: 备用账号

# 全局状态跟踪（自动管理，不要手动编辑）
state:
  codex:
    personal:
      last_used: 2026-03-18T10:30:00Z
      status: active
    work:
      last_used: 2026-03-18T09:00:00Z
      status: cooling
      cooling_until: 2026-03-18T15:00:00Z
```

## 切换方式对比

| 方式 | 适用工具 | 会话连续性 | 实现复杂度 |
|------|----------|-----------|-----------|
| `copy_auth` | codex | ✅ 自动保持 | 低 |
| `env_var` | iflow | ✅ 自动保持 | 低 |

### copy_auth 方式（codex 推荐）

```bash
# 切换流程
on_switch() {
  local profile="$1"
  local auth_file=$(get_profile_auth_file "$profile")
  
  # 1. 备份当前授权
  cp ~/.codex/auth.json ~/.codex/auth.json.bak.$(date +%Y%m%d%H%M%S)
  
  # 2. 复制新授权（如果配置文件也定义了，一并复制）
  cp "$auth_file" ~/.codex/auth.json
  [ -f "$config_file" ] && cp "$config_file" ~/.codex/config.toml
  
  # 3. 重启进程
  kill $pid
  codex resume --last
}
```

**优势**：
- CODEX_HOME 保持不变
- 会话文件位置不变，自动连续
- 无需预先配置软链接

### env_var 方式（iflow）

```bash
# 切换流程
on_switch() {
  local profile="$1"
  local env=$(get_profile_env "$profile")
  
  # 直接注入环境变量启动新进程
  kill $pid
  env $env iflow -c
}
```

**优势**：
- iflow 会话位置固定在 `~/.iflow/history/`
- 切换 `IFLOW_*` 不影响会话文件

## Profile 状态

| 状态 | 说明 | 可用性 |
|------|------|--------|
| `active` | 正常可用 | ✅ |
| `cooling` | 冷却中（限流后） | ❌ 等待冷却结束 |
| `failed` | 认证失败 | ❌ 需要手动修复 |
| `disabled` | 用户禁用 | ❌ |

## 目录结构示例

```
~/.codex-profiles/
├── personal/
│   ├── auth.json      # 个人账号授权
│   └── config.toml    # 个人配置（可选）
├── work/
│   ├── auth.json      # 工作账号授权
│   └── config.toml    # 工作配置
└── backup/
    └── auth.json      # 备用账号授权

~/.codex/              # 主配置目录（切换时被覆写）
├── auth.json          # 当前活跃授权
├── config.toml        # 当前配置
├── sessions/          # 会话文件（位置不变）
└── history.jsonl      # 历史记录
```

## 安全建议

### 授权文件管理

```bash
# 创建 profile 目录并设置权限
mkdir -p ~/.codex-profiles/{personal,work,backup}
chmod 700 ~/.codex-profiles
chmod 600 ~/.codex-profiles/*/auth.json
```

### 备份策略

```bash
# 切换前自动备份（保留最近 5 个）
backup_auth() {
  local backup_dir=~/.codex/backups
  mkdir -p "$backup_dir"
  cp ~/.codex/auth.json "$backup_dir/auth.json.$(date +%Y%m%d%H%M%S)"
  # 清理旧备份，保留最近 5 个
  ls -t "$backup_dir"/*.json | tail -n +6 | xargs rm -f 2>/dev/null
}
```

## CLI 命令

```bash
# 查看当前状态
freely ai-cli status

# 切换 profile
freely ai-cli switch codex work

# 列出所有 profile
freely ai-cli list codex

# 验证配置
freely ai-cli validate

# 备份当前授权
freely ai-cli backup codex
```
