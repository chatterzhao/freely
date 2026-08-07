---
local_id: raw-20260617T031719Z19Z
kind: raw
- phase_state: dropped
platform_ids:
  github:
    issue_id: '2880'
    url: https://github.com/chatterzhao/freely/issues/2880
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T03:17:35Z'
updated_at: '2026-06-17T03:17:35Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 来源
第二轮 subagent 审查发现的 8 个未达标项。

## ACP (5 issues)
1. _read_stderr 不检测 fatal 模式 → _fatal_detected 永不设置
2. _dispatch() 不归一化 stopReason
3. session_ping() 未在 monitor loop 调用
4. _ping_counter 不存在
5. ACP 模式无 per-tool system prompt

## A2A (3 issues)
1. CRITICAL: latest_manager/pending_delivery/launched_pids/add_message/mark_delivered/set_worker_pid 6 个方法通过 JSON-RPC 不可达
2. add_message() → tasks/post 无效方法
3. _http_request 缺少 _stripped guard

## ACP-A2A 协作 (1 issue)
1. _ai_shows_liveness_acp() 缺少 Signal 5 (A2A task 查询)
