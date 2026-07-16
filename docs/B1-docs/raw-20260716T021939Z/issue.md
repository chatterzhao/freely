---
local_id: raw-20260716T021939Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260716T021939Z-A
platform_ids:
  github:
    issue_id: '3925'
    url: https://github.com/chatterzhao/freely/issues/3925
    synced_at: ''
  gitee:
    issue_id: IK1CUV
    url: https://gitee.com/zhaoquan/freely/issues/IK1CUV
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-16T02:20:01Z'
updated_at: '2026-07-16T02:20:01Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因
freely_wt_assert_dev_test_consistent 检测到 dev 有提交未同步到 test 时只报错，不自动修复。导致 pr-create/pr-merge/wt-close 反复因 dev↔test 不同步而阻塞。

## 修复
在 check 2 前自动将 dev 分支 merge 到 test 工位。打印提示日志。
