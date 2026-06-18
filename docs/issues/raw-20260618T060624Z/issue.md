---
local_id: raw-20260618T060624Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T060624Z-A
platform_ids:
  github:
    issue_id: '2978'
    url: https://github.com/chatterzhao/freely/issues/2978
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T06:06:40Z'
updated_at: '2026-06-18T06:06:40Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

pr-review-guarded 在 verdict=pass 时 auto-commit review document，但没有 push。
导致 review commit 留在本地，PR 中没有 review 证据，pr-merge 找不到 review document。

## 当前行为

```
pr-create → push commit A → 创建 PR (指向 A)
pr-review → verdict=pass → commit review doc (commit B) → 提示 git push（未执行）
pr-merge → 查 PR 分支 → 找不到 review doc → 阻塞
```

## 期望行为

```
pr-create → push → 创建 PR (指向 A)
pr-review → verdict=pass → commit review doc (commit B) → auto-push → PR 更新 (A+B)
pr-review → verdict=fail → 阻塞，不 commit 不 push
pr-merge → 查 PR 分支 → 找到 review doc → verdict=pass → 合并
```

## 修复

pr-review-guarded verdict=pass 分支中，git commit 后执行 git push（推送到所有非 all remote）。

GitHub PR 跟踪分支而非 commit——新 commit 推送到同名分支后 PR 自动包含。
