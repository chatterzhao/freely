---
local_id: raw-20260705T072052Z
kind: raw
phase_state: absorbed
platform_ids:
  gitee:
    issue_id: IJYUBF
    url: https://gitee.com/zhaoquan/freely/issues/IJYUBF
    synced_at: ''
primary_platform: gitee
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-05T15:21:20+08:00'
updated_at: '2026-07-05T15:21:20+08:00'
intake_id: ''
author: platform
channel: gitee
session_refs: []
---

\n\n## 问题
.freely/run/a2a-server.log 使用 >> append 模式，无 rotation，运行数月后达到 68GB 撑爆磁盘。

## 根因
daemon 启动 A2A server 时用 >> 追加，而 ACP bridge 有 _truncate_log 清空旧日志，A2A server 没有。

## 修复
daemon 启动 A2A server 前 truncate: : > a2a-server.log
