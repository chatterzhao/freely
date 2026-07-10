---
local_id: raw-20260622T234854Z54Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260622T234854Z-A
platform_ids:
  github:
    issue_id: '3372'
    url: https://github.com/chatterzhao/freely/issues/3372
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T23:49:11Z'
updated_at: '2026-06-22T23:49:11Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## Post-review quality improvements

### 1. #3340 延伸: pr-create-guarded / pr-merge-guarded 改用 platform-adapter
- pr-create-guarded 当前直接调用 `gh pr create`，应改为调用 `platform-adapter create-pr`
- pr-merge-guarded 当前直接调用 `gh pr merge`，应改为调用 `platform-adapter merge-pr`

### 2. #3302 延伸: freely chat 层增加 issue 状态检查
- 当前只在 `platform-adapter.add_comment()` 检查
- 应在 `freely chat --issue <id>` CLI 层增加本地 phase_state 检查

### 3. 孤儿分支清理
- 清理残留的 fix/raw-* 和 test-pre-merge-* 分支

## Acceptance Criteria
- pr-create-guarded 通过 platform-adapter 创建 PR
- pr-merge-guarded 通过 platform-adapter 合并 PR
- freely chat 在发评论前检查 issue phase_state
- 无残留孤儿分支
