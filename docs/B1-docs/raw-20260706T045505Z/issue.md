---
local_id: raw-20260706T045505Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3767'
    url: https://github.com/chatterzhao/freely/issues/3767
    synced_at: ''
  gitee:
    issue_id: IJZ02B
    url: https://gitee.com/zhaoquan/freely/issues/IJZ02B
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-06T04:55:26Z'
updated_at: '2026-07-06T04:55:26Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

\n\n## 问题
issue 已 absorbed 后，wt-create 拒绝创建工位，报"已关闭"。
需要手动去 develop 改 phase_state → 违反 develop 不可写原则。

## 方案
wt-create 检测到 phase_state=absorbed:
1. 自动在工位分支上将 issue.md phase_state 改为 proposed
2. 在 git 历史中记录 reopen 操作
3. 不碰 develop
