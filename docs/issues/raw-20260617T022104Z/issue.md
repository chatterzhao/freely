---
local_id: raw-20260617T022104Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2876'
    url: https://github.com/chatterzhao/freely/issues/2876
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T02:21:21Z'
updated_at: '2026-06-17T02:21:21Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 来源

三组 subagent 独立审查 #2873 ACP/A2A 重构，发现以下未达标项。

---

## ACP 层（3 个 BLOCKER/HIGH）

### B1 (BLOCKER): bridge_lost_marker 变量名 Bug
**文件**: `monitor-ai-acp.sh:413-414`
```bash
[[ -n "$bridge_lost_marker" ]] && echo "bridge_session_lost" > "$bridge_lost_marker"
```
变量应为 `$bridge_lost_marker_file`。当前 `$bridge_lost_marker` 未定义（空字符串），marker 文件**永不写入**。bridge 死亡时上层无法感知。

### H1 (HIGH): `_fatal_detected` 从未设置为 True
**文件**: `acp-bridge.py:127`
`_fatal_detected` 初始化为 False，但没有任何代码路径将其设为 True。`session_prompt()` 的 fatal error 检测是死代码。

### H2 (HIGH): `session_prompt()` stopReason 归一化被绕过
**文件**: `acp-bridge.py:516-534 vs 639`
`session_prompt()` 方法中有正确的 stopReason 归一化逻辑，但 socket client 路径（`handle_client()` → `_send_request()`）完全绕过它，直接返回原始 stopReason。

### H3 (HIGH): `session_ping()` 从未被调用
**文件**: `acp-bridge.py:504-514`
`session_ping()` 存在且正确实现（重置 `last_activity_ts`），但整个代码库中零调用。注释说"A2A workers 应周期性调用此方法"——从未实现。

### M1 (MEDIUM): idle timeout 对 A2A worker 零感知
**文件**: `acp-bridge.py:417-431`
900s 超时仅监控 `last_activity_ts`。Manager 等 Worker 时被误判为 idle。

---

## A2A 层（5 个 CRITICAL）

### C1 (CRITICAL): REST→JSON-RPC 方法映射错误
**文件**: `a2a_task.py:113-131`
`GET /tasks/{id}` 映射为 `tasks/list` 而非 `tasks/get`。`PATCH /tasks/{id}` 映射为 `tasks/push` 非标准方法。

### C2 (CRITICAL): Unix/TCP 传输协议不一致
**文件**: `a2a_task.py:109 vs 151`
Unix socket 走 JSON-RPC POST /，TCP 走直接 REST。同一 `create()` 调用在不同传输层产生不同 wire format。

### C3 (CRITICAL): `save()` 仅在 SUBMITTED 调用，WORKING/COMPLETED 不持久化
**文件**: `a2a_server.py:240,268`
`FreelyAgentExecutor.execute()` 只在初始提交时调 `save()`。WORKING→COMPLETED 状态转换只发 `enqueue_event()`，不调 `save()`。状态不落盘，崩溃丢失。

### C4 (CRITICAL): `freely-db-cli task.*` 绕过 A2A Server
**文件**: `freely-db-cli:376-383`
`task.upsert/get/update/list` 直连 SQLite daemon，完全跳过 A2A Server 的 TaskStore 和协议校验。

### C5 (CRITICAL): SSE streaming 声明但无实现
**文件**: `a2a_server.py:82`
AgentCard 声明 `streaming=True`，但无 SSE endpoint、无 `PendingTask` 实例化、无 stream 路由。

---

## ACP↔A2A 协作层（2 个 GAP）

### G1: `_ai_shows_liveness()` 不查询 A2A task 状态
**文件**: `freely:12922-12997`
liveness 检测只看进程/套接字/日志 mtime。不检查"是否有 alive A2A worker"。

### G2: Worker 完成检测是脆弱日志解析
**文件**: `freely:12691-12765`
`worktree_has_active_worker()` tail 读最后 32KB 日志 + `a2a_task.py extract` 解析。非查询 A2A Server TaskStore。没有 SSE push 通知。

---

## Acceptance Criteria

### ACP
- [ ] `bridge_lost_marker_file` 变量名修复，bridge 死亡可检测
- [ ] `_fatal_detected` 在 bridge 检测到 fatal error 时设为 True
- [ ] socket client 路径应用 stopReason 归一化
- [ ] `session_ping()` 被 A2A-aware 路径周期性调用

### A2A
- [ ] `_unix_request` REST→JSON-RPC 映射修正（get→tasks/get, push→正确方法）
- [ ] Unix/TCP 传输统一为 JSON-RPC 2.0
- [ ] `save()` 在每次状态转换（WORKING/COMPLETED）时调用
- [ ] `freely-db-cli task.*` 改为通过 A2A Server（或明确标注为内部 WAL 专用）
- [ ] SSE endpoint 实现或 `streaming=False`

### ACP↔A2A
- [ ] `_ai_shows_liveness()` 增加 A2A task 状态查询
- [ ] Worker 完成检测改为查 A2A Server TaskStore 而非日志解析

## Affected Files
1. `acp-bridge.py` — B1, H1, H2, H3, M1
2. `monitor-ai-acp.sh` — B1
3. `a2a_task.py` — C1, C2
4. `a2a_server.py` — C3, C5
5. `freely-db-cli` — C4
6. `freely` — G1, G2
