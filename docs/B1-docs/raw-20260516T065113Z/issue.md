---
local_id: raw-20260516T065113Z13Z
kind: raw
phase_state: dropped
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17 04:47:25+00:00
platform_ids:
  github:
    issue_id: '358'
    url: https://github.com/chatterzhao/freely/issues/358
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T06:51:28Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## raw-20260516T065113Z13Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T065113Z13Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T06:51:13Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T065113Z13Z`。实现前请用 `wt-create --raw-key 20260516T065113Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-16T06:51:13Z"
title: "wt-close 修改了 issue frontmatter 但未提交，导致 develop 残留未提交变更"

## 问题

`wt-close` 在 Phase 2（平台关闭）和 Phase 3（force-close trace）中通过 `_fm_set_str` 修改了 `docs/issues/<issue_id>/issue.md` 的 frontmatter（写入 `platform_state: closed`、`force_closed_at` 等），但这些修改**没有提交**。

由于 `wt-close` 在 develop（主工位）执行，这些 frontmatter 变更直接落在 develop 工作区，变成未提交的 dirty state。develop 的 pre-commit hook 又禁止直接在 develop 提交，导致这些变更只能留在工作区，或者被 `git checkout` 丢弃后丢失治理记录。

## 预期行为

`wt-close` 的完整流程应该是：
1. Dry-run 门禁检查
2. 平台同步关闭 issue
3. **提交 frontmatter 更新**（platform_state=closed 等）到合适的 ref
4. 删除远程分支
5. 删除 worktree + 本地分支

提交方式选择：
- 方案 A：在 feature worktree 中提交（修改 feature 分支上的 issue 文件），merge 到 develop 时自然带入
- 方案 B：在 develop 上提交（需要绕过 pre-commit hook 或使用 special commit path）

## 影响

- 每次 wt-close 都会在 develop 留下未提交的 frontmatter 变更
- 治理记录可能丢失（被 git checkout 丢弃）
- 依赖后续 scan 或其他机制来修复不一致

## 范围

改 `docs/system/workspace/scripts/worktree/wt-close`，在 frontmatter 修改后自动提交。
