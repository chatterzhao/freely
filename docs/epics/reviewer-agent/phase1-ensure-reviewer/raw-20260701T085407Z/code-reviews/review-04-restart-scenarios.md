# Review 04: Restart Scenarios + ACP Session Modes

- owner_issue: raw-20260701T085407Z
- date: 2026-07-01

## 两种重启场景

### 1. Freely Restart（daemon 整体重启）

```
整个 freely daemon 停了再启动。所有 agent 都需要恢复。

恢复策略：
  Runtime 启动 → 读 agent_working 表 → 找到所有活跃 agent
  对每个 agent 判断用哪种 ACP session 模式。
```

| Agent 状态（重启前） | ACP 模式 | 条件 | 说明 |
|---------------------|---------|------|------|
| Manager (任何状态) | session/resume | session-store 有记录 | 恢复巡逻上下文 |
| Manager (无记录) | session/new | 首次启动 | 全新巡逻 |
| Worker state=working | session/resume | session-store 有 JSONL 证据 | 继续当前 skill |
| Worker state=working | session/new | 无 session 证据 | 重新开始当前 skill |
| Worker state=input-required | session/resume | 等待 reviewer | 保持等待状态 |
| Reviewer state=working | session/resume | 有审查上下文 | 继续审查 |
| Reviewer state=working | session/new | 无上下文 | 重新审查 |
| Reviewer state=input-required | session/resume | 等待 worker 重做 | 保持等待 |

### 2. Agent Restart（单个 agent 崩溃）

```
某个 agent 进程崩溃，其他正常运行。
Runtime Watchdog 检测到 agent 消失 → 重新启动。
```

| 场景 | 检测方式 | ACP 模式 | 说明 |
|------|---------|---------|------|
| Manager 崩溃 | supervisor 心跳超时 | session/resume | 恢复巡逻 |
| Worker 崩溃 (working) | agent_working.session_get 返回 session 但进程不存在 | session/resume 或 session/new | 优先 resume，无证据则 new |
| Worker 崩溃 (input-required) | 同上 | session/resume | 保持等待，reviewer 还在 |
| Reviewer 崩溃 | 同上 | session/new | 重新审查（审查轻量，不保存上下文） |

## ACP Session 模式选择决策树

```
agent 需要启动
  │
  ├─ session-store 有记录 + JSONL 证据完整？
  │   ├─ 是 → session/resume
  │   └─ 否 → 往下
  │
  ├─ 有 parent session 可以 fork？
  │   ├─ 是 + 同 tool → session/fork
  │   └─ 否或跨 tool → session/new
  │
  └─ 兜底 → session/new
```

## 与 Three-Loop 的关系

Freely 的 three-loop 生命周期：
- Loop 1: scan/discovery（发现待办）
- Loop 2: execution（执行 skill）
- Loop 3: verification/closeout（验证、收口）

重启时需要知道 agent 在哪个 loop：

| Loop | Agent | 重启后行为 |
|------|-------|----------|
| L1 | Manager | session/resume → 重新巡逻 |
| L2 | Worker (working) | session/resume → 继续 skill |
| L2 | Worker (input-required) | session/resume → 等待 reviewer |
| L2 | Reviewer (working) | session/new → 重新审查 |
| L3 | Worker (completed) | 不需要重启（已完成） |
| L3 | Manager (收口中) | session/resume → 继续 wt-close 判断 |

## 当前实现缺口

| 缺口 | 说明 |
|------|------|
| session-store 读写 | _restore_tasks 只恢复 A2A task 状态，不恢复 ACP session |
| agent 崩溃检测 | 无心跳机制，无 watchdog 监控单个 agent 进程 |
| session/resume 路径 | _ensure_reviewer_agent 只写 log，无实际 ACP 启动 |
| agent_working.session_ids | 列值格式支持 session 记录，但无代码写入或读取 |
