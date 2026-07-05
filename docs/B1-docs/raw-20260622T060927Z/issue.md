---
local_id: raw-20260622T060927Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260621T130954Z-A
platform_ids:
  github:
    issue_id: '3341'
    url: https://github.com/chatterzhao/freely/issues/3341
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T06:09:44Z'
updated_at: '2026-06-22T06:09:44Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

以下文件直接调 `gh`/`gitee-issue.py` 而不通过 `platform-adapter.py`，导致平台逻辑分散、无法统一读 `FREELY_REPO_PLATFORMS` 配置。

| 文件 | 直接调用数 |
|------|----------|
| `issue-sync` | 63 |
| `task-lifecycle-scan.py` | 34 |
| `pr-merge-guarded` | 22 |
| `pr-create-guarded` | 13 |
| `wt-create` | 8 |
| `wt-close` | 7 |

## 设计

所有平台 CLI 调用应通过 `platform-adapter.py`，统一读 `FREELY_REPO_PLATFORMS` 配置。优先重构高频文件（`issue-sync`、`task-lifecycle-scan.py`）。

## 涉及文件

同上表，按优先级排序。

🤖 Generated with [Claude Code](https://claude.com/claude-code)
