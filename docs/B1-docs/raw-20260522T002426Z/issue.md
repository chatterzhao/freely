---
local_id: raw-20260522T002426Z26Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2103'
    url: https://github.com/chatterzhao/freely/issues/2103
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-22T00:24:41Z'
updated_at: '2026-06-17T00:25:31Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed---

## 问题
_on_supervisor_err（freely:19092）每次崩溃无条件调用 `freely feedback` 新建 issue。
3天产生950+条 "supervisor crash: bash rc=1"，淹没真实开发issue。

## 修复
在 `_on_supervisor_err` 中加去重逻辑：
1. 用 crash 标题（如 "supervisor crash: bash rc=1"）搜索已有 OPEN issue
2. 如找到 → `gh issue comment` 追加时间戳和出现次数
3. 如未找到 → 新建 issue

用 `gh` CLI 直接操作，不经过 `freely feedback`，因为 feedback 每次新建。
