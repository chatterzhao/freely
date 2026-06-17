# Brainstorm: ACP/A2A 架构重构

## Discovery

### 触发
深度分析 Freely 运行时发现三层协议错位：
1. A2A Server（官方 SDK，JSON-RPC）空转，"Invalid HTTP request" 刷屏
2. Worker 委派绕过 A2A，走 ACP fork + 文件系统
3. kill -9 / 断电后 task 状态全丢，重启后不可恢复
4. ACP idle timeout 不感知 A2A task 状态，Manager 等 Worker 被误杀

### 当前架构 vs 目标架构

**当前（断裂）**：
```
ACP (opencode)  ← 正常工作
A2A Server     ← 空转（协议不匹配，无 agent 连接）
SQLite         ← a2a_task.py --db 绕过全部层直连
Worker         ← ACP fork，不通过 A2A
```

**目标（统一）**：
```
ACP → State Bridge → A2A Server (内存 TaskStore 权威)
                   → 异步 freely-db-cli → db_manager → SQLite WAL
Worker → A2A tasks/send + tasks/push → TaskStore → WAL
```

### 影响面
- 6 个文件：a2a_task.py, a2a_server.py, freely-db-cli, monitor-ai-acp.sh, acp-bridge.py, freely
- 15 处 `a2a_task.py --db` 需改为 JSON-RPC → A2A Server
- 3 个已吸收 issue：#2820 #2821 #2814

## Research

### 现有 SQLite 抽象（必须复用）
| 层 | 文件 | 行数 | 状态 |
|---|------|------|------|
| Daemon | `freely_db_manager.py` | 1426 | ✅ a2a_tasks 表已定义 |
| CLI | `freely-db-cli` | 384 | ⚠️ 需新增 task-upsert/task-restore/task-list |
| Server | `a2a_server.py` (L107) | 540 | ⚠️ 已知 db socket，未使用 |

### 三种 AI CLI tool 差异
opencode / claude / codex 在 `tool-launchers.sh` 中无 capability 区分。需新增 per-tool system prompt 注入。

### A2A 协议合规
| 标准要求 | 当前 | 目标 |
|---------|------|------|
| JSON-RPC 2.0 | ❌ REST | ✅ |
| AgentCard | ❌ | ✅ |
| TaskStore 内存权威 | ❌ 空转 | ✅ |
| 异步 WAL 持久化 | ❌ | ✅ |
| SSE streaming | ❌ | ✅ |
| WAL replay 崩溃恢复 | ❌ | ✅ |

## Decision

### 方案：统一 JSON-RPC + 事件溯源 WAL

**Phase A: A2A 协议 + 持久化**
- freely-db-cli 新增 task 操作（复用 db_manager）
- a2a_task.py 改 JSON-RPC 2.0，移除 --db
- A2A Server: 状态变更 → 异步调 db-cli → WAL
- 15 处 --db 调用改为 JSON-RPC → A2A Server

**Phase B: ACP 状态暴露**
- session/ping heartbeat, stopReason 正规化, per-tool prompt

**Phase C: State Bridge**
- idle timeout 前查内存 TaskStore

**Phase D: Worker A2A 标准化**
- Worker 走 tasks/send + tasks/push

### 降级策略
SQLite 不可用 → 纯内存运行（WAL 写 skip），不阻塞。SQLite 恢复后补写。

### 风险
- JSON-RPC 迁移影响 15 处调用 → 需充分测试
- A2A Server 异步 WAL 新增 → 不影响现有 ACP 路径
- 低风险：ACP 层改动（heartbeat + stopReason）是增量添加
