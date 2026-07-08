---
local_id: raw-20260708T202402Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3828'
    url: https://github.com/chatterzhao/freely/issues/3828
    synced_at: ''
  gitee:
    issue_id: IJZS0M
    url: https://gitee.com/zhaoquan/freely/issues/IJZS0M
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-08T20:24:24Z'
updated_at: '2026-07-08T20:24:24Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

lifecycle-v3 (801 行) 从 bak.py (2007 行) 重构时丢失了 4 个核心设计：

### 1. 两级 [manager]/[worker] 委派模式
旧 scan 每条 next_action 有两级：

新 scan 只有一级 [manager] 模糊指令：批量修正
