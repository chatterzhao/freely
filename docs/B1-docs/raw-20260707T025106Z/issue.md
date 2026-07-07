---
local_id: raw-20260707T025106Z
kind: raw
phase_state: absorbed
absorbed_into: 'I-20260707T025106Z-A'
platform_ids:
  github:
    issue_id: '3790'
    url: https://github.com/chatterzhao/freely/issues/3790
    synced_at: ''
  gitee:
    issue_id: IJZA9D
    url: https://gitee.com/zhaoquan/freely/issues/IJZA9D
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-07T02:51:06Z'
updated_at: '2026-07-07T02:51:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

pr-create-guarded 有 Step 0a 工位清洁检查，但 pr-review-guarded 缺少对应检查。
review 过程中如果产生文件修改（如 review 文档写回、gate 修复等），这些修改可能未被提交就被 merge 或丢失。

## 需要修复

1. pr-review-guarded 增加工位清洁检查（审查前 + 审查后）
2. 确保每个阶段结束时工位必须是 clean 的
