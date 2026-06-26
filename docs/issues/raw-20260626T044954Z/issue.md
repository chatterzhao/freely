---
local_id: raw-20260626T044954Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3539'
    url: https://github.com/chatterzhao/freely/issues/3539
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T04:50:14Z'
updated_at: '2026-06-26T04:50:14Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

agent-id.env 已统一文件命名，但命令行参数仍用 `--worker-id`，暗示只有 worker 需要这个参数。应该用 `--agent-id`，三种 agent 平等。

## 改动
```
bin/freely-review: --worker-id → --agent-id
bin/agent-table-query: --get-reviewer <agent_id> 已正确
pr-review-guarded: 调用改为 --agent-id
manager-agent.md: 文档同步
```

## 不改
- agent-table.toml 字段名 (manager_id/worker_id/reviewer_id 是具体字段，保持不变)
- agent-id.env 文件名（已正确）
