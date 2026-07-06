# Tasks: ACP/A2A 架构重构

- issue_id: I-20260617T011030Z-A
- status: in_progress

## Phase A: A2A 协议 + 持久化（P0 基础）

### A-1: freely-db-cli 新增 task 操作
- status: pending
- file: `docs/system/workspace/scripts/runtime/freely-db-cli`
- 新增 subcommands: task-upsert, task-restore, task-list
- 复用 db_manager 已有 a2a_tasks 表

### A-2: a2a_task.py 改 JSON-RPC 2.0
- status: pending
- file: `docs/system/workspace/scripts/runtime/a2a_task.py`
- `_unix_request()` 发送 JSON-RPC 2.0
- 移除 `--db` 参数及相关逻辑

### A-3: A2A Server 集成异步 WAL
- status: pending
- file: `docs/system/workspace/scripts/runtime/a2a/a2a_server.py`
- TaskStore 状态变更 → 异步调 db-cli task-upsert
- 启动时 db-cli task-restore → WAL replay
- 复用 L107 已有 db socket

### A-4: freely 脚本 --db 调用改为 JSON-RPC
- status: pending
- file: `docs/system/workspace/scripts/runtime/freely`
- 15 处 `a2a_task.py --db` 改为 JSON-RPC → A2A Server

## Phase B: ACP 状态暴露（P0）

### B-1: session/ping + stopReason
- status: pending
- files: `acp-bridge.py`, `monitor-ai-acp.sh`

### B-2: Per-tool system prompt
- status: pending
- files: `tool-launchers.sh`, `freely`

## Phase C: State Bridge（P1）

### C-1: idle timeout ↔ TaskStore
- status: pending
- file: `freely`

## Phase D: Worker A2A 标准化（P1）

### D-1: Worker tasks/send + tasks/push
- status: pending
- files: `freely`, `a2a_task.py`, `a2a_server.py`
