---
local_id: I-20260617T063755Z-A
kind: linked
status: in_dev
phase_state: completed
promoted_from: raw-20260617T063755Z
source_candidate: docs/pre-brainstorms/20260617T063755Z--a2a-unified-data-flow/candidates.md
canonical_issue_path: ''
platform_ids: {}
primary_platform: ''
last_synced_comment_at: {}
hash: ''
created_at: 2026-06-17 06:37:55+00:00
updated_at: 2026-06-17 06:40:00+00:00
intake_id: ''
author: zhaoquan
channel: freely-fix-execution
session_refs: []
pre_tests_path: docs/epics/a2a-unified-data-flow/pre-tests.md
verification_artifact_dir: docs/epics/a2a-unified-data-flow/code-reviews
platform_state: closed
---

# I-20260617T063755Z-A: A2A Unified Data Flow

- source_candidate: `docs/pre-brainstorms/20260617T063755Z--a2a-unified-data-flow/candidates.md`
- branch: `fix/raw-20260617T063755Z-a2a-unified-data-flow`

## 修复

1. **a2a_task.py**: 6 个 Freely 方法从 `_db_rpc()` 改为 `_request()` → A2A Server。移除客户端 `_db_rpc` 方法。
2. **a2a_server.py**: streaming=True, push_notifications=True, 新增 SSE endpoint `/tasks/{id}/stream`，状态变更自动通知订阅者。

## 架构
```
freely → a2a_task.py → A2A Server (内存权威) → async db-cli → SQLite WAL
```
