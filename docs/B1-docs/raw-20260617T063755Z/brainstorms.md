# Brainstorm: A2A Unified Data Flow

## Discovery
raw-20260617T011030Z30Z Phase A 规定的目标架构未完全实现：
- `_db_rpc` 在 `a2a_task.py` 中绕过了 A2A Server，直接操作 SQLite
- SSE 流式推送零实现
- SQLite 被用作实时协调通道，而非设计的异步 WAL

## Decision
**Promote**。问题明确，修复简单：a2a_task.py 6 个方法改为通过 A2A Server，启 SSE。
