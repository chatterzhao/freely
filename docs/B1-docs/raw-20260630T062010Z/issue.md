---
local_id: raw-20260630T062010Z10Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260630T062010Z-A
platform_ids:
  github:
    issue_id: '3643'
    url: https://github.com/chatterzhao/freely/issues/3643
    synced_at: ''
  gitee:
    issue_id: IJXT2A
    url: https://gitee.com/zhaoquan/freely/issues/IJXT2A
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-30T06:20:30Z'
updated_at: '2026-06-30T06:20:30Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 问题

1. Phase 3.6: wt-close 复制 raw issue 到 develop——越权且无效（develop 是保护分支）
2. --force help 没说清楚：如果觉得已 merge 应该用不带 force 的正常 wt-close，报错说明没 merge

## 改动
- 移除 Phase 3.6（复制文件到 develop）
- --force help 明确：只有一个目标=彻底丢弃
- Block 消息强化：如果认为已 merge → 不带 force 重试 → 报错=没 merge → STOP
