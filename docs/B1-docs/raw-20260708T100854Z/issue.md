---
local_id: raw-20260708T100854Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260708T100854Z-A
platform_ids:
  github:
    issue_id: '3818'
    url: https://github.com/chatterzhao/freely/issues/3818
    synced_at: ''
  gitee:
    issue_id: IJZQ77
    url: https://gitee.com/zhaoquan/freely/issues/IJZQ77
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T10:09:15Z'
updated_at: '2026-07-08T10:09:15Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因

A2A server 绑定的 socket 路径是 `/tmp/freely-a2a-{hash}`
a2a_task.py 连接的路径是 `/tmp/freely-a2a-{hash}.sock`
SSE watchdog 连接的路径是 `/tmp/freely-a2a-{hash}.sock`

路径不一致导致 A2A 通信完全断开。Manager 能启动（ACP 正常），但无法委派 Worker（A2A 断路）。

## 影响

整个多 agent 协作瘫痪：
- Manager 无法创建 A2A task
- Worker 无法被委派
- SSE 事件流断开
- Reviewer 无法被触发

## 修复

统一 socket 路径命名——要么 server 加上 .sock，要么 client/watchdog 去掉。

## 需要排查

- A2A server 代码中 socket 创建逻辑
- a2a_task.py 中 socket 路径
- watchdog_sse.py 中 socket 路径
- sse-watchdog.sh 中 socket 路径
- freely shell 中 `_a2a_socket_path` 函数
