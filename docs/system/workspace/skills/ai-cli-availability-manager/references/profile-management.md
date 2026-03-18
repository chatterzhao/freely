# Profile 配置规范

本文档定义 Freely 管理 AI CLI profile 的配置格式和规范。

## 配置文件位置

全局配置文件：`~/.config/freely/ai-cli-profiles.yaml`

项目级覆盖（可选）：`<project>/.env/ai-cli-profiles.yaml`

## 授权文件目录

**统一存放位置**：`~/.ai-auth/`

```
~/.ai-auth/
├── codex-personal/
│   └── auth.json
├── codex-work/
│   └── auth.json
├── codex-backup/
│   └── auth.json
├── iflow-default/
│   └── settings.json      # 包含 apiKey
└── iflow-backup/
    └── settings.json
```

**命名规则**：`<tool>-<account-name>/`

## 配置格式

```yaml
# AI CLI Profile 配置
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
      backup:
        auth_dir: ~/.ai-auth/codex-backup
        description: 备用账号
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
          IFLOW_baseUrl: https://apis.iflow.cn/v1
      backup:
        env:
          IFLOW_apiKey: $IFLOW_BACKUP_KEY
          IFLOW_baseUrl: https://apis.iflow.cn/v1

# 状态跟踪（自动管理）
state:
  codex:
    personal:
      last_used: 2026-03-18T10:30:00Z
      status: active
    work:
      status: cooling
      cooling_until: 2026-03-18T15:00:00Z
```

## 切换方式

### codex: copy_auth

```bash
# 切换流程
switch_codex_profile() {
  local profile="$1"
  local auth_dir=$(get_profile_auth_dir "$profile")  # ~/.ai-auth/codex-work
  
  # 备份当前授权
  cp ~/.codex/auth.json ~/.codex/auth.json.bak
  
  # 复制新授权
  cp "$auth_dir/auth.json" ~/.codex/auth.json
  
  # 重启进程
  kill $pid
  codex resume --last
}
```

### iflow: env_var

```bash
# 切换流程
switch_iflow_profile() {
  local profile="$1"
  local env=$(get_profile_env "$profile")
  
  kill $pid
  env $env iflow -c
}
```

## 目录结构

```
~/.ai-auth/                    # 统一授权文件目录
├── codex-personal/auth.json
├── codex-work/auth.json
├── codex-backup/auth.json
├── iflow-default/settings.json
└── iflow-backup/settings.json

~/.codex/                      # codex 主目录（切换时覆写）
├── auth.json                  # 当前活跃授权
├── config.toml
├── sessions/                  # 会话文件（位置不变）
└── history.jsonl

~/.iflow/                      # iflow 主目录（不变）
├── settings.json
├── history/                   # 会话文件（位置不变）
└── ...
```

## 用户准备步骤

### codex

```bash
# 1. 创建授权目录
mkdir -p ~/.ai-auth/codex-personal
mkdir -p ~/.ai-auth/codex-work

# 2. 用对应账号登录 codex，然后复制授权文件
# 登录账号1后：
cp ~/.codex/auth.json ~/.ai-auth/codex-personal/

# 登录账号2后：
cp ~/.codex/auth.json ~/.ai-auth/codex-work/

# 3. 设置权限
chmod 700 ~/.ai-auth
chmod 600 ~/.ai-auth/*/auth.json
```

### iflow

```bash
# iflow 使用环境变量，在 ~/.zshrc 或 ~/.bashrc 中设置
export IFLOW_DEFAULT_KEY="sk-xxxxx"
export IFLOW_BACKUP_KEY="sk-yyyyy"
```

## CLI 命令

```bash
# 查看当前状态
freely ai-cli status

# 切换 profile
freely ai-cli switch codex work

# 列出所有 profile
freely ai-cli list

# 验证配置
freely ai-cli validate

# 从当前登录账号保存到 profile
freely ai-cli save codex personal
```
