---
local_id: raw-20260516T075140Z40Z
kind: raw
phase_state: absorbed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '359'
    url: https://github.com/chatterzhao/freely/issues/359
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T07:51:56Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-16T07:55:38Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
absorbed_into: raw-20260710T005219Z---

## raw-20260516T075140Z40Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T075140Z40Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T07:51:40Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T075140Z40Z`。实现前请用 `wt-create --raw-key 20260516T075140Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-16T07:51:40Z"
title: "pre-commit hook 不支持 FREELY_SKIP_IBM_GATE 豁免，导致 wt-close 无法自动提交 frontmatter"

## 问题

`pre-commit.sh` 对 `main|develop` 分支的直接提交没有检查 `FREELY_SKIP_IBM_GATE`，导致 #358 的 wt-close auto-commit 功能被拦截。

```bash
case "$branch" in
  main|develop)
    # 缺少 FREELY_SKIP_IBM_GATE 检查
    if git rev-parse --verify MERGE_HEAD ...; then
      ...
    fi
    # 直接提交直接到这里被拦截
    [HOOK] Commit blocked: direct development on 'develop' is forbidden.
```

## 修复

在 `main|develop` case 的开头加入 FREELY_SKIP_IBM_GATE 豁免——和 pre-push.sh 的 `[HOOK] IBM governance gate skipped` 模式一致。

## 范围

只改 `docs/system/workspace/hooks/pre-commit.sh` 的 `main|develop` 分支处理逻辑，加一行 FREELY_SKIP_IBM_GATE 检查。
