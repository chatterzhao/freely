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
    # 当前活跃 profile
    active: personal
    
    # profile 定义
    profiles:
      personal:
        # 环境变量注入
        env:
          CODEX_HOME: ~/.codex-personal
        # 描述（可选）
        description: 个人账号
        # 标签（可选，用于分组）
        tags: [personal, primary]
        
      work:
        env:
          CODEX_HOME: ~/.codex-work
        description: 工作账号
        tags: [work]
        
      backup:
        env:
          CODEX_HOME: ~/.codex-backup
        description: 备用账号
        tags: [backup]
    
    # profile 选择策略
    strategy:
      # 轮询策略：round-robin, random, priority
      mode: round-robin
      # 排除正在冷却的 profile
      skip_cooling: true
  
  iflow:
    active: default
    profiles:
      default:
        env:
          IFLOW_apiKey: sk-default-key
          IFLOW_baseUrl: https://apis.iflow.cn/v1
        description: 默认账号
        
      backup:
        env:
          IFLOW_apiKey: sk-backup-key
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
      status: cooling  # 冷却中
      cooling_until: 2026-03-18T15:00:00Z
```

## Profile 状态

| 状态 | 说明 | 可用性 |
|------|------|--------|
| `active` | 正常可用 | ✅ |
| `cooling` | 冷却中（限流后） | ❌ 等待冷却结束 |
| `failed` | 认证失败 | ❌ 需要手动修复 |
| `disabled` | 用户禁用 | ❌ |

## 环境变量作用域

Freely 在启动 AI CLI 子进程时注入环境变量，不污染当前 shell 环境：

```bash
# 错误方式：污染全局环境
export CODEX_HOME=~/.codex-personal
codex

# 正确方式：仅注入子进程
CODEX_HOME=~/.codex-personal codex
```

## 配置验证规则

1. **至少一个 profile**：每个工具必须定义至少一个 profile
2. **env 必须是字典**：env 字段必须是键值对
3. **路径必须存在**：环境变量中的路径必须存在且可访问
4. **不包含敏感信息**：配置文件中不应包含 API key 明文（使用环境变量引用）

## 安全建议

### API Key 管理

不要在配置文件中直接写入 API key：

```yaml
# 不推荐
profiles:
  personal:
    env:
      IFLOW_apiKey: sk-xxxxx  # 明文暴露

# 推荐：引用环境变量
profiles:
  personal:
    env:
      IFLOW_apiKey: $IFLOW_PERSONAL_KEY  # 引用外部变量
```

然后在 `~/.zshrc` 或 `~/.bashrc` 中：
```bash
export IFLOW_PERSONAL_KEY="sk-xxxxx"
```

### 配置文件权限

```bash
chmod 600 ~/.config/freely/ai-cli-profiles.yaml
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
```
