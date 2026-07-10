---
local_id: raw-20260627T084545Z23Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3584'
    url: https://github.com/chatterzhao/freely/issues/3584
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
absorbed_into: I-20260627T084523Z-A
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-27T08:45:44Z'
updated_at: '2026-06-27T08:45:44Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## Scope

Agent 生命周期管理：agent-id.env 僵尸清理、sync_tooling 并发控制、wt-close ACP session/close。

## Bugs

- Bug A: agent-id.env 38 个僵尸条目（工位已删但记录还在）
- Bug B: sync_tooling 永远分配 worker_01，pool 未利用
- Bug C: sync_tooling 绕过 max_parallel_workers 10:7 限流
- Bug D: git worktree remove --force 跳过所有清理
- Bug E: wt-close 不发送 ACP session/close RPC

## Changes

- freely: 委派前调 manager_reconcile_agent_id_env
- freely:5877: round-robin 选空闲 worker
- freely:sync_tooling: 加并发检查
- wt-close:Phase6: 调 _acp_session_close
