---
local_id: raw-20260625T045412Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3479'
    url: https://github.com/chatterzhao/freely/issues/3479
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T04:54:31Z'
updated_at: '2026-06-25T04:54:31Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T045412Z-A
source_candidate: docs/pre-brainstorms/20260625T045412Z--migrate-to-adapter/candidates.md#C-20260625T045412Z-A
---

## 问题

当前各命令各自实现平台操作，加平台要改多份代码。

## 迁移清单

| 命令 | 当前 | 改为 |
|------|------|------|
| feedback | gh + gitee-issue.py | adapter create-issue |
| issue-sync | _gh_* + _gitee_call | adapter create/update/close/comment |
| crash reporter | gh 直接调用 | adapter search + comment |
| wt-close | issue-sync close（≠adapter） | adapter close |
| pr-review | gh pr list | adapter |
| pr-merge | gh pr close | adapter close-pr |
| _fill_platform_ids | 重复 adapter pull 逻辑 | 去重，信任 pull |

## 依赖

#3478（adapter 补 CLI）

## 收益

加 GitCode：只需 adapter 加 _gitcode_* 函数。上述 7 处零改动。
