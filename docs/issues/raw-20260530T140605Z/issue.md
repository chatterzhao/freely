---
local_id: raw-20260530T140605Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '2342'
    url: https://github.com/chatterzhao/freely/issues/2342
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-30T14:06:19Z'
updated_at: '2026-05-30T14:06:19Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 修复

1. task-lifecycle-scan.py: 将 platform_close 和 branch_deleted 加入 add_platform_sync_batch 的 sync_stages。这些项的 next_action 与批量同步一致，66 个 branch_deleted 不再逐条列出，汇总到单个 batch（653 items: pull=411 push=10 reconcile=181 close=51）

2. start-lead-agent.sh: 移除 additional_requirements_escaped 注入。manager-agent.md 已由 build_prompt 通过 Agent 角色定义 header 注入，重复注入导致 ~141 行冗余

## 效果
- Scan items: 197 → 82 (-58%)
- Scan JSON: 174KB → 64KB
- Prompt 治理段落去重: ~141 行
- 预计 prompt 从 85KB → ~55KB
