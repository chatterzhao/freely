# Review 07: Agent 间通信 — Session 活跃 vs 不活跃

- owner_issue: raw-20260701T085407Z
- date: 2026-07-01

## 两种通信模式

### 模式 A：Session 活跃（A2A 直连，像聊天窗口追加消息）

```
双方 ACP session 都在运行:

  Worker (ACP session 活跃)          Reviewer (ACP session 活跃)
      │                                    │
      │──PATCH /tasks {state:input-required, reason:needs-review:b1}
      │                                    │
      │         a2a_tasks                  │
      │        ┌──────────┐               │
      │        │ SSE push │               │
      └────────▶          ◀───────────────┘
                └──────────┘
                       │
              Reviewer 的 ACP session 收到 SSE 事件
              → 就像聊天窗口收到新消息
              → ACP session/prompt 追加: "Worker 的 B1 完成了，请审查"
              → Reviewer 审查 → PATCH verdict
              → SSE push → Worker ACP session 收到
              → "Reviewer 说: pass, 继续 B2"
```

**效果**：就像两个人开着聊天窗口，不断收发消息。
Runtime 完全不参与——agent 之间直连 A2A SSE。

### 模式 B：Session 不活跃（Runtime 启动 ACP）

```
目标 agent 的 ACP session 不存在或已死:

  Runtime Watchdog 检测到 needs-review:b1
      │
      ├─ agent_working 查 reviewer 的 session
      │   ├─ 有 session_id 且进程存活? → session/resume
      │   ├─ 有 session_id 但进程死了? → session/new
      │   ├─ 同 tool + parent session 活跃? → session/fork
      │   └─ 无任何记录? → session/new
      │
      └─ ACP session 创建后 → agent 启动
          → 然后进入模式 A（直连通信）
```

## ACP 模式选择决策

```
需要启动 agent
  │
  ├─ session-store 有 session_id + 进程存活？
  │   └─ YES → session/resume（恢复对话历史）
  │       "你之前审查到一半，继续"
  │
  ├─ 同 tool + parent session 活跃？
  │   └─ YES → session/fork（复用 ACP 连接，轻量）
  │       "从 Manager 的 session fork 一个新的"
  │
  └─ 以上都不满足
      └─ session/new（全新启动）
          "你是 Reviewer，审查这个 B1"
```

## 具体场景举例

### 场景 1: Worker 做完 B1，Reviewer 已经在运行

```
Worker → PATCH input-required
  → SSE push → Reviewer 收到（模式 A：直连，像聊天追加消息）
  → Reviewer ACP prompt 追加: "审查 B1"
  → Reviewer 审查完成 → PATCH completed
  → SSE push → Worker + Manager 收到
Runtime: 零参与 ✅
```

### 场景 2: Worker 做完 B1，Reviewer 还没启动

```
Worker → PATCH input-required
  → SSE push → Runtime Watchdog 收到
  → agent_working 查: reviewer 无 session
  → ACP session/new（模式 B：Runtime 启动）
  → Reviewer 启动 → 收到 prompt: "审查 B1"
  → 之后进入模式 A（直连）
Runtime: 启动 agent 后退出 ✅
```

### 场景 3: freely restart，Worker 做到一半

```
Daemon 重启
  → _restore_tasks 恢复 A2A task 状态
  → agent_working 查 worker_03: session_id=ses_def456
  → session-store 查: ses_def456 有 JSONL 证据
  → ACP session/resume（恢复对话）
  → Worker 继续: "你之前在 B1，产物已保存，继续"
Runtime: resume 后退出 ✅
```

### 场景 4: Reviewer 崩溃，Worker 在等

```
Runtime Watchdog 心跳检测: reviewer_05 进程不存在
  → agent_working 查: reviewer_05 的 session_id 存在但进程死
  → ACP session/new（无有效 session 证据，全新启动）
  → Reviewer 启动: "审查 raw-KEY 的 B1"
  → 进入模式 A
Runtime: 检测 + new + 退出 ✅
```

## 关键认知

```
ACP session/prompt = agent 的"聊天窗口"
A2A SSE = agent 之间的"消息推送"

session 活跃 → A2A SSE 追加消息（聊天窗口继续对话）
session 不活跃 → ACP session/new|fork|resume（重新打开聊天窗口）
                     → 然后 A2A SSE 追加消息
```

Runtime 的职责：维护 agent 的"聊天窗口"（ACP session）。
Agent 的职责：在聊天窗口里对话（A2A SSE）。
