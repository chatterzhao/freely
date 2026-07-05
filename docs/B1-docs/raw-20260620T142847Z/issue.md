---
local_id: raw-20260620T142847Z47Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T142847Z-A
platform_ids:
  github:
    issue_id: '3174'
    url: https://github.com/chatterzhao/freely/issues/3174
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T14:29:05Z'
updated_at: '2026-06-21T20:14:35Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

### 1. pr-review-guarded 不认工位

当前 `pr-review-guarded` 在 L20 执行 `cd "$ROOT_DIR"`（git root），然后在 develop root 里跑 governance-merge-gate。Gate 读的是 develop 的 docs/，没有 fix 分支新增的 governance 文件 → IBM Completeness 误报失败。

应该根据 branch 名找到对应工位，在工位内执行 gate。

### 2. 生成 review doc 不填 issue_id

pr-review-guarded 自动生成 pr-review-xxx.md 不包含 `- issue_id`，导致 pr-merge-guarded 的 gate 又报 "owner issue missing"。应该从 branch 名解析 raw-key → 查 I-* issue → 自动填入。

## 修复

### pr-review-guarded 工位检测

```
输入: branch name → 解析 raw-key → 查找 fix 工位路径
  → cd 到工位 → 在工位内跑 governance-merge-gate
```

新增 `--worktree` 参数（可选的显式指定），无参数时自动从 branch 名推断：
1. `git worktree list` 找 branch 对应的路径
2. 校验工位存在且 clean
3. 在该工位上下文中执行 gate

### 自动生成 issue_id

解析 branch 名提取 raw-key（如 `fix/raw-20260618T091116Z16Z-xxx` → `20260618T091116Z`），查找 `docs/issues/I-{key}-*/issue.md`，提取 `issue_id`，写入 review doc。

### 无参数校验

`review_branch="${1:-}"` — 不传 branch 参数时报错退出，提示用法。

## 影响文件
- `bin/pr-review-guarded` — 工位检测 + 自动 issue_id + 参数校验
