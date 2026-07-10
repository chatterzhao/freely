---
local_id: raw-20260618T051709Z09Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T051709Z-A
platform_ids:
  github:
    issue_id: '2974'
    url: https://github.com/chatterzhao/freely/issues/2974
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T05:17:26Z'
updated_at: '2026-06-18T05:17:26Z'
intake_id: ''
author: platform
channel: github
session_refs: []

platform_state: closed---

## Bug

PR #2967 的 review gate 代码从未写入 pr-merge-guarded。Python 字符串替换静默失败（和 #2970 develop check 一样的问题）。

pr-merge-guarded 缺少对 pr-review-guarded 产物的检查——合并前不验证 review verdict。

## Fix

在 PR gate 之后、run_promotion_gate 之前插入 review gate：
1. 查找 pr-review-{PR#}.md
2. 检查 verdict=pass
3. 不通过则阻塞
