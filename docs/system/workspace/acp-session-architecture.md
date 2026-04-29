# ACP Session Architecture

## 核心变化

```
direct 模式：                    ACP 模式：
claude -p → 新进程 → 退出        claude-agent-acp → 常驻进程
每次发送完整 prompt              session 保持 → 增量交互
PID 退出 = 任务完成              协议消息 = 任务完成
--resume 发送历史 → 贵            session/load → cache hit → 便宜
```

## Session 策略（三级缓存命中）

```
第 1 级：同 session resume（最便宜，几乎免费）
  session/load <same-id> → 全部上下文在内存 → 0 token 成本

第 2 级：新 session 同 system prompt（便宜）
  session/new → system prompt 前缀匹配 → 只收增量 token

第 3 级：新 session 不同 prompt（全价）
  session/new → 无缓存 → 完整收费
```

## Manager 与 Worker 的 Session 模型

```
Manager（主管）:
  首次启动: session/new → 获得 M-session-id
  后续周期: session/load M-session-id（第 1 级缓存）
  委派 worker: 不需要新 session，写 worker prompt 文件即可

Worker（工人）:
  首次启动: session/new → 获得 W-session-id
    首条 prompt 包含 manager 的任务描述（第 2 级缓存——system prompt 相同）
  后续周期: session/load W-session-id（第 1 级缓存）
  完成任务: 写 exit contract → manager 接管

多 Worker 并发:
  Worker-A: session/new → WA-id → session/load WA-id
  Worker-B: session/new → WB-id → session/load WB-id
  各自独立 session，互不干扰
  都共享 system prompt 前缀 → 第 2 级缓存命中
```

## 何时 New vs Resume

```
决策树:

有 CLAUDE_SESSION_ID_CURRENT？
├─ YES → JSONL 证据存在？
│   ├─ YES → session/load（第 1 级缓存）  ← 最优先
│   └─ NO → AI_RESUME_ON_RESTART? → ERROR
│
└─ NO（新 worktree 或 fresh start）
    ├─ 有 SESSION_PARENT_ID？
    │   └─ YES → 这是 worker fork → session/new（第 2 级缓存）
    └─ NO → session/new（首次启动，第 3 级）
```

**与 direct 模式的关键区别**：
- direct 模式：fresh launch 每次都重新发送 60KB system prompt → 贵
- ACP 模式：session/new 也共享 system prompt 前缀 → 第 2 级缓存 → 便宜很多
- ACP 模式下 fresh 不再是灾难，因为 system prompt 前缀在服务端被缓存

## ACP 替代 PID 监控

| direct 模式 | ACP 模式 |
|------------|---------|
| 等 PID 退出 | 等 session/prompt 响应 |
| kill -0 检测存活 | 协议心跳 |
| 进程退出 = 完成 | stopReason = "end_turn" |
| SIGTERM 杀进程 | session/close |

## 需要修改的代码

1. **run-acp-prompt.py** — 支持 session/load（resume）和 session/fork
2. **tool-launchers.sh** — ACP 适配器注入 session-id
3. **freely** — select_launch_kind 适配 ACP 语义
4. **monitor-ai-cli.sh** — ACP 完成检测替代 PID 监控
5. **session-cache.sh** — 统一 session ID 管理（direct 和 ACP 共用）

## 实施优先级

P0: run-acp-prompt.py 支持 session/load + session-id 参数
P1: monitor-ai-cli.sh ACP 完成检测
P1: freely 适配 ACP session 语义
P2: 多 worker session fork 策略
