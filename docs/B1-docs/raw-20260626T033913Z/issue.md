---
local_id: raw-20260626T033913Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3535'
    url: https://github.com/chatterzhao/freely/issues/3535
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-26T03:39:32Z'
updated_at: '2026-06-26T03:56:04Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260626T033913Z-A
source_candidate: docs/B1-docs/raw-20260626T033913Z/candidates.md#C-20260626T033913Z-A
promoted_issue_path: docs/issues/I-20260626T033913Z-A/issue.md
pre_tests_path: docs/B2-docs/freely-review/verification/pre-tests.md
platform_state: closed
---

## 设计

### agent-id.env
位置: .freely/agent-id.env，格式: worktree_path=agent_type=agent_id

### agent-table 格式
[[agents]] manager_id+reviewer_manager_01 pool=1
[[agents]] worker_id+reviewer_worker_01 pool=10

### freely-review --caller worker|manager
worker: ACP sync，pre-check 工位存在+clean+sync
manager: A2A async，pre-check 工位不存在(存在则FAIL，wt-close 失效)

### 改动
- .freely/agent-table.toml: 新格式
- bin/agent-table-query: agent-id.env
- bin/freely-review: 新建
- bin/pr-review-guarded: 改用 freely-review --caller worker
- sync_tooling: 写 agent-id.env
