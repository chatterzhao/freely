---
local_id: raw-20260705T010030Z30Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260705T010030Z-A
platform_ids:
  github:
    issue_id: '3734'
    url: https://github.com/chatterzhao/freely/issues/3734
    synced_at: ''
  gitee:
    issue_id: IJYTMP
    url: https://gitee.com/zhaoquan/freely/issues/IJYTMP
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-05T01:00:51Z'
updated_at: '2026-07-05T01:00:51Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

wt-close 当前支持 --raw-key 和 --branch 两个入口，还存在 test-pre-merge 分支的 disposable 路径。用户直接传 test-pre-merge 分支名会走单独逻辑，破坏了统一性。

## 设计

--raw-key 为唯一必填参数。命令从 raw key 自动发现 fix/feature 和 test-pre-merge 两个工位，按先测试后开发的顺序关闭。

## 改动

1. 移除 --branch 参数
2. 移除 _extract_issue_id 函数（issue_id 始终 = raw-${_raw_key}）
3. 移除 test-pre-merge 分支 disposable 路径
4. usage 和错误提示全部指向 --raw-key
