---
name: freely-ai-cli-availability-manager
description: >-
  Watchdog 控制面中的 availability 子模块。负责 AI CLI 工具的账号可用性检测、
  切号、限流检测与自动恢复探测。

  Use when: AI CLI 工具报认证错误、限流、账号不可用，或需要切换账号。
  触发词："切号"、"限流"、"auth error"、"rate limit"、"认证失败"。
---

# skill:freely-ai-cli-availability-manager

> 这是 `skill:freely-watchdog-control-plane` 的 availability watchdog 子模块。

## 触发条件

1. **启动时**：`freely-auto-loop-orchestrator` 启动 AI CLI 前，注入正确的环境变量
2. **限流时**：监控 AI CLI 输出检测到限流信号
3. **凭证失效**：检测到认证失败或 token 过期

## 核心流程

### 1. 启动注入

```
freely-auto-loop-orchestrator 准备启动 AI CLI
    ↓
调用 skill:freely-ai-cli-availability-manager
    ↓
读取当前活跃 account 配置
    ↓
注入环境变量（如 CODEX_HOME, IFLOW_apiKey）
    ↓
返回环境变量列表给 orchestrator
    ↓
orchestrator 启动 AI CLI
```

### 2. 限流检测与切换（关键流程）

**重要**：已运行的进程无法动态切换账号，必须重启进程。

```
监控 AI CLI 输出
    ↓
匹配限流模式（见 references/limit-patterns.md）
    ↓
记录当前会话 ID 和进度到 recovery
    ↓
标记当前 account 为"冷却中"
    ↓
发送 SIGTERM 终止进程（优雅终止）
    ↓
等待进程退出（最多 5 秒，超时 SIGKILL）
    ↓
选择下一个可用 account
    ↓
注入新环境变量
    ↓
尝试恢复会话（见会话恢复策略）
    ↓
继续循环
```

### 3. 会话恢复策略

按优先级尝试：

```
1. fork/continue 当前会话（推荐）
   - codex: CODEX_HOME=~/.codex-new codex fork <session-id>
   - iflow: IFLOW_apiKey=new-key iflow -c
   
2. resume 最近会话
   - codex: CODEX_HOME=~/.codex-new codex resume --last
   - iflow: IFLOW_apiKey=new-key iflow -r
   
3. 启动全新会话
   - 从 recovery 文件恢复上下文
```

**注意事项**：
- codex 切换 `CODEX_HOME` 后，会话文件可能不在新目录
- 建议配置共享会话目录（见 references/process-lifecycle.md）
- iflow 切换 `IFLOW_*` 变量不影响会话位置，优势明显

### 4. 凭证失效处理

```
检测到认证失败（401/403）
    ↓
记录凭证失效事件
    ↓
标记当前 account 为 failed
    ↓
尝试下一个 account
    ↓
如果所有 account 都失效：
    - 暂停循环
    - 通知用户
    - 等待手动干预
```

## 输入

- `tool`: AI CLI 工具名称（codex/iflow/kiro）
- `action`: `inject` | `switch` | `status`
- `account`: 可选，指定 account 名称
- `session_id`: 可选，当前会话 ID（用于恢复）

## 输出

- `env_vars`: 需要注入的环境变量字典
- `active_account`: 当前活跃的 account 名称
- `event`: 触发的事件（限流/切换/失效）
- `recovery_hint`: 会话恢复提示（session_id + resume 命令）

## 下一跳

- 正常：返回 `freely-auto-loop-orchestrator` 继续执行
- 限流：调用 `freely-recovery-subagent-governance` 记录事件后继续
- 全部失效：调用 `freely-recovery-subagent-governance` 进入阻塞状态

## References

- [tool-config-matrix.md](references/tool-config-matrix.md) - 各工具的配置模式
- [limit-patterns.md](references/limit-patterns.md) - 限流检测模式
- [account-management.md](references/account-management.md) - Account 配置规范
- [auth-setup.md](references/auth-setup.md) - 授权文件准备与验证
- [process-lifecycle.md](references/process-lifecycle.md) - 进程生命周期与会话恢复
- [cli-interface-design.md](references/cli-interface-design.md) - CLI 接口设计

## 与其他 Skill 的集成

| Skill | 集成方式 |
|-------|----------|
| `freely-constitution-guard` | 预检 account 配置是否完整 |
| `freely-laws-enforcer` | 验证切换事件是否正确记录 |
| `freely-auto-loop-orchestrator` | 提供 AI CLI 启动时的环境变量 |
| `freely-recovery-subagent-governance` | 限流/失效事件触发恢复流程 |
| `freely-watchdog-control-plane` | 作为 umbrella skill 定义 availability / runtime / continuity watchdog 的上层边界 |

## 安全约束

1. **不触碰凭证文件**：Freely 不读取、不复制、不存储凭证
2. **不记录敏感信息**：日志中不包含 token 或 API key
3. **环境变量作用域**：仅注入到 AI CLI 子进程，不污染全局环境
4. **优雅终止**：优先 SIGTERM，超时才 SIGKILL
