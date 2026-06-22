---
local_id: I-20260622T123158Z-A
kind: I
phase_state: completed
platform_ids:
  github:
    issue_id: ''
    url: ''
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T13:30:00Z'
updated_at: '2026-06-22T13:30:00Z'
intake_id: ''
author: claude
channel: local
session_refs: []
---

# I-20260622T123158Z-A: Agent Tool Policy

## PRD

在 manager-agent.md 和 worker-agent.md 中添加 Tool Policy 章节，约束 Agent 的工具使用：
- Manager：禁止 git add/commit/push/merge，禁止 gh 命令，允许 a2a_task.py/a2a-exit
- Worker：允许 git add/commit，禁止 a2a_task.py/a2a-exit/gh

## Tasks

1. 在 manager-agent.md 添加 Tool Policy 章节 ✅
2. 在 worker-agent.md 添加 Tool Policy 章节 ✅

## Pre-tests

- 验证两个文件都包含 Tool Policy 章节 ✅
- 验证 Manager 禁止 git add/commit ✅
- 验证 Worker 禁止 a2a_task.py/a2a-exit ✅

## Code Review

纯文档变更，无代码风险。Tool Policy 内容与 #3363 的子代理评审结论一致。
