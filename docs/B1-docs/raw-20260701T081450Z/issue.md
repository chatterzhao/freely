---
local_id: raw-20260701T081450Z50Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260701T081450Z-A
platform_ids:
  github:
    issue_id: '3695'
    url: https://github.com/chatterzhao/freely/issues/3695
    synced_at: ''
  gitee:
    issue_id: IJY3QF
    url: https://gitee.com/zhaoquan/freely/issues/IJY3QF
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-01T08:15:12Z'
updated_at: '2026-07-01T08:15:12Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

\n\n
## 问题
pr-merge-guarded 锁目录存在但无 pid（孤儿锁）时静默等 300s，无提示。

## 根因
mkdir 和 pid 写入有竞态，进程在之间崩溃留下孤儿锁。acquire_merge_lock 无 pid 时不诊断直接等超时。

## 修复
三种状态：
- 有pid+进程存活 → 阻塞
- 有pid+进程已死 → 自动清理
- 无pid → 自动清理（之前静默等300s）
