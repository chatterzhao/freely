---
local_id: raw-20260622T114625Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260622T114625Z-A
platform_ids:
  github:
    issue_id: '3356'
    url: https://github.com/chatterzhao/freely/issues/3356
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T11:46:42Z'
updated_at: '2026-06-22T11:46:42Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

`--platform-only` 被工作树检查（L262-268）拦截，因为该检查只允许 `--force` 无工作树，没有考虑 `--platform-only` 场景。

## 修复

`--platform-only` 也应该被允许在无工作树的情况下执行。同时优化错误提示，告诉用户可以用 `--platform-only`。

## 涉及

- `docs/system/workspace/scripts/worktree/wt-close` L263

🤖 Generated with [Claude Code](https://claude.com/claude-code)
