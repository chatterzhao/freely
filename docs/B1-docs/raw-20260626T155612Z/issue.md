---
local_id: raw-20260626T155612Z12Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260626T155612Z-A
platform_ids:
  github:
    issue_id: '3565'
    url: https://github.com/chatterzhao/freely/issues/3565
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T15:56:35Z'
updated_at: '2026-06-26T15:56:35Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 现象

pr-merge-guarded 在 merge 到 develop 后，issue-sync 写入 fix worktree
的 issue 文件（platform_state: closed），导致 fix 工位变脏，wt-close 被卡住。

## 根因

_sync_issues_changed_in_merge 在 merge + push develop 之后执行，
--project 指向 fix worktree，写入但未 commit。

对比 review: commit → push → merge → 干净。
当前 issue-sync: merge → push → issue-sync(写脏 fix worktree)。

## 修复

1. 将 _sync_issues_changed_in_merge 移到 merge 之前
2. issue-sync 后自动 commit + push（与 review 一致）
3. diff 比较从 HEAD vs HEAD^ 改为 source vs target
