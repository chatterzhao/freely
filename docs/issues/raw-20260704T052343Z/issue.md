---
local_id: raw-20260704T052343Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3724'
    url: https://github.com/chatterzhao/freely/issues/3724
    synced_at: ''
  gitee:
    issue_id: IJYRBW
    url: https://gitee.com/zhaoquan/freely/issues/IJYRBW
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-04T05:24:13Z'
updated_at: '2026-07-04T05:24:13Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n
## 问题

多处报错信息写 "(use wt-close or wt-close --force to clean up)"，容易让人以为 --force 是常规清理手段。

## 实际语义

- wt-close <branch> — 工作完成收口
- wt-close --force <branch> — 废弃并丢弃该 raw issue 的全部实现

不是废弃坚决禁止使用 --force。有任何门禁报错都是去解决问题，不是用 --force 绕过。

## 需修改位置

1. pre-commit.sh line 29: 孤儿分支提示
2. freely line 16597: completed/zombie worker 提示
absorbed_into: I-20260704T052343Z-A
