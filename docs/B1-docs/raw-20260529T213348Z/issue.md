---
local_id: raw-20260529T213348Z48Z
kind: raw
phase_state: dropped
platform_ids:
  github:
    issue_id: '2317'
    url: https://github.com/chatterzhao/freely/issues/2317
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-29T21:34:06Z'
updated_at: '2026-05-29T21:34:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

Manager AI 委派 worker 时， 中的 prompt 文件路径是相对于 Manager project 的相对路径（如 ）。

 在启动 worker 进程时，先  到目标 worktree，然后传相对路径给 。由于 worker process 的 cwd 是目标 worktree，而  在每个 worktree 中是隔离的（非 git 跟踪），worker 在自己的  下找不到 Manager 写的 prompt 文件。

## 修复

在  函数入口，将相对路径解析为基于 Manager project root 的绝对路径。

## 证据

- Manager prompt 文件存在：
- Worker worktree 下无此文件： 目录不存在
- Worker cycle log: `[ERROR] [Errno 2] No such file or directory: '.freely/run/worker-prompts/...'`
- 同一 worktree 被重复委派 3 次，每次都因同样原因失败
