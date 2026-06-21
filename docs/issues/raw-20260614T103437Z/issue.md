---
local_id: raw-20260614T103437Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '2657'
    url: https://github.com/chatterzhao/freely/issues/2657
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-14T10:34:53Z'
updated_at: '2026-06-21T18:26:20Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## Phase 2b: 合并 a2a_task.py / a2a_client.py
- 两个独立实现合并为一个标准 A2A 客户端
- 删除 a2a_client.py，功能移入 a2a_task.py

## Phase 3: Session Store 扩展
- session_rounds 表 (SQLite) 替代 cycle-*.log 文件
- freely-db-cli session.export-jsonl / import-jsonl
- freely-db-cli session.get-last-exit-kind (Bash 兼容)
- 90天 TTL 清理策略

## Phase 4: 废弃文本 JSON 解析
- a2a_task_parser.py 标记 deprecated
- 保留为 fallback-only，添加 deprecation 日志
