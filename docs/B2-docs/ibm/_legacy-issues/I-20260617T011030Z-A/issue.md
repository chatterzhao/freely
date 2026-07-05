---
local_id: I-20260617T011030Z-A
kind: linked
status: completed
phase_state: completed
promoted_from: raw-20260617T011030Z
source_candidate: docs/B1-docs/raw-20260617T011030Z/candidates.md
canonical_issue_path: ""
platform_ids: {}
primary_platform: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-06-17T01:10:30Z
updated_at: 2026-06-17T01:10:30Z
intake_id: ""
author: zhaoquan
channel: freely-feat-execution
session_refs: []
pre_tests_path: docs/B2-docs/acp-a2a-refactor/verification/pre-tests.md
verification_artifact_dir: docs/B2-docs/acp-a2a-refactor/code-reviews
---

# I-20260617T011030Z-A: ACP/A2A 架构重构

- source_candidate: `docs/B1-docs/raw-20260617T011030Z/candidates.md`
- pre_tests_path: `docs/B2-docs/acp-a2a-refactor/verification/pre-tests.md`
- verification_artifact_dir: `docs/B2-docs/acp-a2a-refactor/code-reviews`
- milestone: M-20260617T011030Z-A

## 实现

### Phase A: A2A 协议 + 事件溯源 WAL
1. `freely-db-cli` 新增 task-upsert / task-restore / task-list（复用 db_manager 的 a2a_tasks 表）
2. `a2a_task.py` `_unix_request()` 改为 JSON-RPC 2.0，移除 `--db` 直连
3. `a2a_server.py` TaskStore 状态变更 → 异步调 db-cli → WAL
4. `freely` 脚本 15 处 `a2a_task.py --db` 改为 JSON-RPC → A2A Server

### Phase B: ACP 状态暴露
1. `acp-bridge.py` 新增 session/ping
2. `monitor-ai-acp.sh` 30s heartbeat + stopReason 正规化
3. `tool-launchers.sh` / `freely` per-tool system prompt 注入

### Phase C: State Bridge
1. `freely` idle timeout 前查 A2A Server TaskStore（内存）

### Phase D: Worker A2A 标准化
1. Worker 通过 tasks/send + tasks/push 收发

## Implementation Decision Note

见 `docs/B2-docs/acp-a2a-refactor/code-reviews/implementation-decision.md`
