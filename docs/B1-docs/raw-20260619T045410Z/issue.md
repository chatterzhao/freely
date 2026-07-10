---
local_id: raw-20260619T045410Z10Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T045410Z-A
source_candidate: docs/B1-docs/raw-20260619T045410Z10Z/candidates.md#C-20260619T045410Z-A
platform_ids:
  github:
    issue_id: '3030'
    url: https://github.com/chatterzhao/freely/issues/3030
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T04:54:26Z'
updated_at: '2026-06-19T04:54:26Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## 问题

`pr-merge-guarded` (in `docs/system/workspace/scripts/worktree/pr-merge-guarded`) 在合并确认之前就关闭了 GitHub PR：

```
L497-498: gh pr close $_pr          ← 先关了 PR
L501:     git merge --no-commit     ← 然后做 merge
L506:     git merge --continue      ← 触发 pre-merge-commit hook
          → hook 失败 → merge abort → PR 已 close，无法恢复
```

## 影响

当 governance gate (pre-merge-commit hook) 因治理文档不达标而拦截合并时，PR 已经被 close。用户修复问题后必须重新走 pr-create-guarded → pr-review-guarded 全流程，浪费大量时间。

## 修复方向

1. **方案 A（推荐）**: 先尝试 dry-run merge（或实际 merge + hook 验证），全部通过后再 `gh pr close` + 正式 commit
2. **方案 B**: hook 失败时自动 `gh pr reopen` 恢复 PR
3. **方案 C**: 用 `git merge --no-commit` 但不触发 hook，手动验证 governance gate 后再继续

## 涉及文件

- `docs/system/workspace/scripts/worktree/pr-merge-guarded` — 主要修改文件
