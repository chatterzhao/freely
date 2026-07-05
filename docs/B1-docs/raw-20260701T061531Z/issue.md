---
local_id: raw-20260701T061531Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260701T061531Z-A
platform_ids:
  github:
    issue_id: '3690'
    url: https://github.com/chatterzhao/freely/issues/3690
    synced_at: ''
  gitee:
    issue_id: IJY1UR
    url: https://gitee.com/zhaoquan/freely/issues/IJY1UR
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-01T06:15:53Z'
updated_at: '2026-07-01T06:15:53Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n
## 问题

governance-merge-gate 的 lifecycle 错误逐条散落输出，skill 引用内嵌在每条错误中。用户需要逐条读才能知道看哪个 skill。

## 修复

在错误列表末尾增加按 skill 分组的汇总：

```
── 需要阅读的 Skill ──
  skill:freely-doc-B1_IBM-execution §门禁常见坑速查 (3 个错误)
  skill:freely-doc-B2_IBM-execution §门禁常见坑速查 (5 个错误)

── 错误详情 ──
  [B1] absorbed_into missing in raw-xxx
  [B1] milestone binding missing for C-xxx
  [B2] promoted_issue_path missing for C-xxx
  ...
```
