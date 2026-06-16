---
local_id: raw-20260613T052111Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2581'
    url: https://github.com/chatterzhao/freely/issues/2581
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-13T05:21:27Z'
updated_at: '2026-06-13T05:21:27Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题
1. a2a_server.py --stop CLI 只 rm socket，不杀进程
2. stop_project_runtime() 无 DB daemon 停止逻辑

## 修复
对齐 JiuwenSwarm PID file + SIGTERM signal 模式

## 验证
- start → PID file 写入 ✅
- stop → SIGTERM → should_exit → 进程退出 ✅
- 进程残留检查 ✅
