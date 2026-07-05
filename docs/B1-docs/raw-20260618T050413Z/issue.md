---
local_id: raw-20260618T050413Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260618T050413Z-A
platform_ids:
  github:
    issue_id: '2972'
    url: https://github.com/chatterzhao/freely/issues/2972
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-18T05:04:29Z'
updated_at: '2026-06-18T05:04:29Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 当前行为

Step 0a 用两个命令检查：

1. `git status --porcelain | grep -v '^?'` — 跟踪文件的修改（M/A/D/R）
2. `git ls-files --others --exclude-standard` — 所有未跟踪未忽略的文件

## 问题

`git ls-files --others --exclude-standard` 过于激进——会拦截所有不在 .gitignore 中的文件，包括：
- 编辑器临时文件（*.swp, *~）
- 系统文件（.DS_Store）
- 构建产物（如果 .gitignore 不完整）

这些文件不应该阻塞 pr-create。

## 真正要防止的

**commit 遗漏**——应该提交但忘记 git add 的文件。最常见场景：
- wt-create 拉取的 `docs/B1-docs/raw-*/issue.md` 忘记 add
- B1_IBM/B2_IBM 产出的 `docs/B1-docs/raw-`, `docs/epics/` 文件忘记 add
- 修改的源码忘记 add

## 修复方向

方案 A: 把 `git ls-files --others` 限制到治理目录


方案 B: 直接使用 `git status --porcelain`（不过滤 ??），但提供更清晰的 guidance  
方案 C: `git status --porcelain` + 只 warn 不 block untracked 文件
