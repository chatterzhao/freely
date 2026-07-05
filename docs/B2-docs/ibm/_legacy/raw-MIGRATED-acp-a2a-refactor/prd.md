# PRD: ACP/A2A 架构重构

## Goal

统一 ACP/A2A 协议层到最标准形态。A2A 走 JSON-RPC 2.0 + 事件溯源 WAL（复用 db_manager）。
ACP 新增 heartbeat + stopReason 正规化 + per-tool prompt。Worker 走 A2A 标准委派。

## Scope

### In
- a2a_task.py REST → JSON-RPC 2.0，移除 --db
- freely-db-cli 新增 task 操作
- A2A Server TaskStore + 异步 WAL
- ACP session/ping + stopReason + per-tool prompt
- State Bridge（idle timeout ↔ TaskStore）
- Worker tasks/send + tasks/push

### Out
- 不替换 db_manager（复用现有）
- 不改变 ACP bridge 核心协议（session/prompt/resume 不变）
- 不删除 prompt 文件 fallback 机制

## Non-functional
- 内存更新不阻塞（WAL 异步 fire-and-forget）
- 降级：SQLite 不可用 → 纯内存 + WAL skip
- 崩溃恢复：WAL replay → TaskStore 重建
- 三种 AI CLI 同等支持

## Dev-Loop Handoff
- Phase A 优先（基础），B/C/D 可并行
- 15 处 --db 调用需逐一改为 JSON-RPC
- 每 Phase 完成后 gov-gate check
