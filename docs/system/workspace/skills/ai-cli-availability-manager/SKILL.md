---
name: ai-cli-availability-manager
description: 管理 AI CLI 工具的可用性，包括账号切换、限流检测和恢复集成。当 AI CLI 遇到限流或凭证问题时自动切换到备用账号。
---

# skill:ai-cli-availability-manager

## 触发条件

1. **启动时**：`auto-loop-orchestrator` 启动 AI CLI 前，注入正确的环境变量
2. **限流时**：监控 AI CLI 输出检测到限流信号
3. **凭证失效**：检测到认证失败或 token 过期

## 核心流程

### 1. 启动注入

```
auto-loop-orchestrator 准备启动 AI CLI
    ↓
调用 skill:ai-cli-availability-manager
    ↓
读取当前活跃 profile 配置
    ↓
注入环境变量（如 CODEX_HOME, IFLOW_apiKey）
    ↓
返回环境变量列表给 orchestrator
    ↓
orchestrator 启动 AI CLI
```

### 2. 限流检测与切换

```
监控 AI CLI 输出
    ↓
匹配限流模式（见 references/limit-patterns.md）
    ↓
记录限流事件到 recovery
    ↓
标记当前 profile 为"冷却中"
    ↓
选择下一个可用 profile
    ↓
注入新环境变量
    ↓
重启 AI CLI 会话
    ↓
继续循环
```

### 3. 凭证失效处理

```
检测到认证失败（401/403）
    ↓
记录凭证失效事件
    ↓
尝试下一个 profile
    ↓
如果所有 profile 都失效：
    - 暂停循环
    - 通知用户
    - 等待手动干预
```

## 输入

- `tool`: AI CLI 工具名称（codex/iflow/kiro）
- `action`: `inject` | `switch` | `status`
- `profile`: 可选，指定 profile 名称

## 输出

- `env_vars`: 需要注入的环境变量字典
- `active_profile`: 当前活跃的 profile 名称
- `event`: 触发的事件（限流/切换/失效）

## 下一跳

- 正常：返回 `auto-loop-orchestrator` 继续执行
- 限流：调用 `recovery-subagent-governance` 记录事件后继续
- 全部失效：调用 `recovery-subagent-governance` 进入阻塞状态

## References

- [tool-config-matrix.md](references/tool-config-matrix.md) - 各工具的配置模式
- [limit-patterns.md](references/limit-patterns.md) - 限流检测模式
- [profile-management.md](references/profile-management.md) - Profile 配置规范

## 与其他 Skill 的集成

| Skill | 集成方式 |
|-------|----------|
| `constitution-guard` | 预检 profile 配置是否完整 |
| `laws-enforcer` | 验证切换事件是否正确记录 |
| `auto-loop-orchestrator` | 提供 AI CLI 启动时的环境变量 |
| `recovery-subagent-governance` | 限流/失效事件触发恢复流程 |

## 安全约束

1. **不触碰凭证文件**：Freely 不读取、不复制、不存储凭证
2. **不记录敏感信息**：日志中不包含 token 或 API key
3. **环境变量作用域**：仅注入到 AI CLI 子进程，不污染全局环境
