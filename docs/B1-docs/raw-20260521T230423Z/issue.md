---
local_id: raw-20260521T230423Z23Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2100'
    url: https://github.com/chatterzhao/freely/issues/2100
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-21T23:04:36Z'
updated_at: '2026-06-17T00:23:58Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-22T09:19:38Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## 问题

append_task_source_patrol_seed_if_needed 第15012行 `active_running_workers > 0 → return` 对所有路径生效。只要有1个常驻worker（如stale-pid-keepalive），scan永不可见。

原始设计(41c60594)是基于backlog≥5跳过scan，语义合理。active_running_workers guard后来加入但过宽。

## 修复

在 append_task_source_patrol_seed_if_needed 中区分路径：
- fresh/fork: 不受 active_running_workers 影响，始终展示scan
- prompt(delta): 有活跃worker时跳过scan（Manager已知上下文，先处理worker汇报）

方案：增加一个可选参数 `--skip-if-active-workers`，只在prompt路径传入。
