# Implementation Decision Note: ACP/A2A 架构重构

- issue_id: I-20260617T011030Z-A
- reviewer: claude-sonnet-4-6
- review_date: 2026-06-17

## Decision

采用 **JSON-RPC 2.0 + 事件溯源 WAL** 一次性重构 A2A 协议层，复用现有 `freely_db_manager.py` + `freely-db-cli` 抽象。ACP 层新增 heartbeat + stopReason + per-tool prompt。

## Why This

1. **JSON-RPC 2.0** 是 A2A 官方 SDK 的协议标准。当前 REST 客户端与 JSON-RPC 服务端不匹配是 A2A Server 空转的根本原因。
2. **事件溯源 WAL** 保证 kill -9 后状态可恢复。每次状态变更先更新内存（零延迟），再异步写 SQLite（不阻塞）。
3. **复用 db_manager** 不另起炉灶。a2a_tasks 表已定义，只需在 db-cli 加 3 个操作。
4. **一次性重构** 不过渡。15 处 --db 调用全部改为 JSON-RPC，不留兼容代码。

## Alternatives Considered

### Alternative A: A2A Server 兼容 REST
- 在 A2A Server 新增 REST routes 适配当前客户端
- Rejected: 偏离 A2A 官方 SDK 标准，两端都要改，更复杂

### Alternative B: 渐进迁移（REST + JSON-RPC 并存）
- 新旧客户端并存，逐步迁移
- Rejected: 代码复杂度翻倍，过渡期维护困难

### Alternative C: 仅修复协议，不做 WAL
- 只修 JSON-RPC，不碰持久化
- Rejected: 崩溃恢复是基础能力，不等下一轮

## Boundary Check

- CONSTITUTION.md: 不涉及分支/worktree 边界
- LAWS.md: 不涉及 skip governance
- ACP Protocol: session/prompt/resume 不变，只加 session/ping
- db_manager: 不修改 schema，只通过 db-cli 新增操作

## Non-Goals

- 不替换 db_manager 为其他存储
- 不改变 Worker prompt 文件格式
- 不删除 prompt 文件 fallback

## Residual Risk

- **低风险**: JSON-RPC 迁移影响 15 处调用 → 逐一验证
- **低风险**: 异步 WAL 写失败 → 内存状态继续，不影响运行
- **无风险**: ACP 改动（heartbeat + stopReason）是增量，不影响现有路径
