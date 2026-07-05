---
local_id: raw-20260625T211802Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3513'
    url: https://github.com/chatterzhao/freely/issues/3513
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T21:18:21Z'
updated_at: '2026-06-25T21:18:21Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T211802Z-A
source_candidate: docs/B1-docs/20260625T211802Z--agent-table-slot-chain/candidates.md#C-20260625T211802Z-A
promoted_issue_path: docs/issues/I-20260625T211802Z-A/issue.md
pre_tests_path: docs/epics/agent-table-slot-chain/verification/pre-tests.md
---

## 设计

当前 agent-table.toml 已定义池但未被完整消费。需要补全：

### 1. agent-table-query 加空闲检测
```
--next-free worker  → 扫所有工位 .freely/worker-id.env 得 busy，返回第一个空闲 worker
--get-reviewer <worker_id> → 返回 reviewer_id + reviewer_slot  
--list-manager → 返回 manager_id + manager_slot
```

### 2. sync_tooling 写 worker-id.env
wt-create → sync_tooling:
- 调 `--next-free worker` 拿空闲 worker_id
- 写 `.freely/worker-id.env: worker_id=worker_03`
- 写 `slot=worker_slot` 到 config.toml（已有，改用 --next-free 替代 head -1）

### 3. pr-review-guarded 读 reviewer_slot
- 读 `.freely/worker-id.env` → worker_id
- `agent-table-query --get-reviewer <worker_id>` → reviewer_slot
- ACP 用 reviewer_slot 启动 Reviewer

### 4. Manager daemon start 读 manager_slot
- agent-table-query --get manager_01 → manager_slot
- 覆盖 develop 工位 config.toml 的 AI_TOOL

### 5. manager_max_parallel_workers 读 agent-table
- 用 pool count 代替硬编码 10:7
- warn threshold = count * 0.7
