---
local_id: raw-20260705T064047Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260705T064047Z-A
platform_ids:
  github:
    issue_id: '3743'
    url: https://github.com/chatterzhao/freely/issues/3743
    synced_at: ''
  gitee:
    issue_id: IJYU6Y
    url: https://gitee.com/zhaoquan/freely/issues/IJYU6Y
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-05T06:41:08Z'
updated_at: '2026-07-05T06:41:08Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题
三个 develop 保护点的拦截消息不一致：
1. dirty 提示有重复行，指引被截断
2. pre-merge-commit 只说 pr-merge-guarded，没有指向工作流
3. 应统一为：临时就丢弃，不是就走 freely feedback → freely wt-create → skill

## 修复
三个保护点统一消息模式
