---
local_id: raw-20260626T025748Z48Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3533'
    url: https://github.com/chatterzhao/freely/issues/3533
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T02:58:07Z'
updated_at: '2026-06-26T04:16:37Z'
intake_id: ''
author: platform
channel: github
session_refs: []
pre_tests_path: docs/B2-docs/a2a-review-states/verification/pre-tests.md
absorbed_into: I-20260626T025748Z-A

platform_state: closed---

## 设计

### 1. A2A/SSE Worker→Reviewer 状态流
- 新增 exit_kind: `worker_in_review` → working
- pr-review-guarded 内部每轮结果通过 SSE push 到 Manager
- Manager 可见 review 进度（哪一轮、pass/fail/剩余轮数）

### 2. wt-close help 文本 fix→fix|feature
- 3 处 help 示例只写 fix/raw-xxx，补充 feature/raw-xxx

## 改动
- a2a_task.py: exit_kind 映射新增 worker_in_review
- pr-review-guarded: SSE push review 状态
- sse-watchdog.sh: 识别 review 状态
- exit-kind-mapping.md: 文档更新
- docs/system/workspace/scripts/worktree/wt-close: help 文本 fix|feature
