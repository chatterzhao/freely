---
local_id: raw-20260618T065221Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T065221Z-A
platform_ids:
  github:
    issue_id: '2981'
    url: https://github.com/chatterzhao/freely/issues/2981
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T06:52:38Z'
updated_at: '2026-06-18T06:52:38Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 根因

`gh pr merge --merge --body` 无效。`--body` 仅在 `--squash`/`--rebase` 时生效，`--merge` 时 GitHub 自己生成 "Merge pull request #XXXX" 消息，body 被丢弃。

证据：所有通过 `gh pr merge` 创建的 merge commit 都没有 `Freely-Merge-Path` receipt。reference-transaction hook 拦截 pull → 手动 reset → origin 落后 → 下一个工位拿到旧代码。

## 修复

`pr-merge-guarded` 改用 local `git merge --no-ff`：

```
git fetch github develop
git merge --no-ff <branch> -m "Merge branch '<branch>' into develop

Freely-Merge-Path: pr-merge-guarded"
git push github develop && git push origin develop
```

- receipt 在 commit message 中 → hook 放行
- 所有平台收到相同 merge commit → 不再分叉
- GitHub PR 在 push 后自动检测到合并并关闭

## 同时修复

wt-create 行 627: `git fetch origin 2>/dev/null` 吞错误。
应验证所有平台 develop HEAD 一致，不一致时清晰报错阻塞。
