---
local_id: raw-20260617T124129Z29Z
kind: raw
phase_state: dropped
platform_state: closed
completed_at: '2026-08-07T06:00:00Z'
closeout_note: 'legacy raw closeout (platform closed)'
platform_ids:
  github:
    issue_id: '2922'
    url: https://github.com/chatterzhao/freely/issues/2922
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-17T12:41:47Z'
updated_at: '2026-06-17T14:29:07Z'
intake_id: ''
author: platform
channel: github
session_refs: []
force_closed_at: '2026-06-17T14:29:07Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## 问题
wt-close 用 FREELY_SKIP_IBM_GATE=1 在 develop 上直接 commit frontmatter 更新（force_closed_at, phase_state）。commit 后不 push，导致 develop 变脏，阻塞后续 git pull --ff-only。

正确设计：frontmatter 更新应在 pr-merge-guarded 阶段完成——此时已知道 raw_key/I-issue，改完合入 merge commit 一起推送。

## 方案
pr-merge-guarded 在 merge 后、push 前：
1. 更新 raw issue 的 frontmatter（phase_state=absorbed, absorbed_into=I-xxx，force_closed_at）
2. 更新 I-issue 的 frontmatter（phase_state=completed）
3. git add docs/issues/ + commit --amend（吸收到 merge commit）
4. push all remotes

wt-close 简化为：
1. 校验 phase_state（已由 pr-merge-guarded 更新，通常已完成）
2. 关平台 issue（GitHub API close）
3. git worktree remove
4. git branch -d（不再需要 -D）

## 影响文件
- docs/system/workspace/scripts/worktree/pr-merge-guarded：新增 frontmatter 更新逻辑
- docs/system/workspace/scripts/worktree/wt-close：移除 frontmatter commit 逻辑
