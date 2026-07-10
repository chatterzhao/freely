---
local_id: raw-20260625T153111Z11Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3508'
    url: https://github.com/chatterzhao/freely/issues/3508
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T15:31:32Z'
updated_at: '2026-06-25T15:31:32Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T153111Z-A
source_candidate: docs/B1-docs/raw-20260625T153111Z11Z/candidates.md#C-20260625T153111Z-A
promoted_issue_path: docs/issues/I-20260625T153111Z-A/issue.md
pre_tests_path: docs/B2-docs/agent-table/verification/pre-tests.md

platform_state: closed---

## 设计

```toml
# .freely/agent-table.toml

[[agents]]
manager_id = "manager_01"
manager_slot = "claude-apikey-ds-pro-auto"
worktree = "develop"

[[agent_pools]]
role = "worker"
count = 10
worker_slot = "claude-apikey-ds-sonnet-auto"
reviewer_slot = "opencode-apikey-ds-haiku-auto"
```

Runtime 展开：
```
worker_01 ↔ reviewer_01
worker_02 ↔ reviewer_02
...
worker_10 ↔ reviewer_10
```

- `[[agents]]` 声明单例（Manager）
- `[[agent_pools]]` 声明池（Worker+Reviewer 配对），count=10 自动编号
- `{role}_slot` 是终端已配好的 alias，对应 provider+model+key
- wt-create 读表为工位写入对应的 AI_TOOL
- Manager 委派时查表中空闲的 worker_id → 拿到配对 reviewer_id 和 slot

## 实现
- .freely/agent-table.toml 格式 + 解析
- wt-create 集成：读 agent-table 取 slot
- Manager patrol 集成：读 agent-table 查空闲 worker
