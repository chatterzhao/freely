---
local_id: raw-20260624T105442Z42Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260624T105442Z-A
platform_ids:
  github:
    issue_id: '3429'
    url: https://github.com/chatterzhao/freely/issues/3429
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-24T10:54:59Z'
updated_at: '2026-06-24T10:54:59Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 根因
wt-close Phase 6 用 `git branch -d $branch` 删除分支。不加 ref 参数时，git 检查 upstream 或 HEAD。这些 fix/feature 分支无 upstream，fallback 到 HEAD——但在 worktree 中 HEAD 即分支自身，永远判定"not merged"，每次都退到 `-D`。

L372 的 `_ahead` 检查（`rev-list --count develop..$branch`）已正确判定合并状态。`-d` 和 `_ahead` 看的是不同 ref。

## 修复
`git branch -d "$branch"` → `git branch -d "$branch" develop`

wt-close 已 cd 到 PROJECT_ROOT，develop ref 是主 repo 的最新 develop（含 merge commit），检查结果与 _ahead 一致。
