---
local_id: raw-20260625T152446Z46Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3507'
    url: https://github.com/chatterzhao/freely/issues/3507
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-25T15:25:06Z'
updated_at: '2026-06-25T15:25:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
absorbed_into: I-20260625T152446Z-A
source_candidate: docs/B1-docs/raw-20260625T152446Z46Z/candidates.md#C-20260625T152446Z-A
promoted_issue_path: docs/issues/I-20260625T152446Z-A/issue.md
pre_tests_path: docs/B2-docs/pr-review-acp-reviewer/verification/pre-tests.md
platform_state: closed
---

## 设计

pr-review-guarded 从"bash 自审打勾"改为"启动独立 Reviewer agent 评审"：

```
Worker (fix/xxx, session A)
  │
  pr-review-guarded:
    │
    ├─ 读 agent-table → 找到 worker 绑定的 reviewer_id → review_slot
    ├─ 收集上下文: pre-tests.md + git diff + issue
    │
    ├─ round=1: ACP session/new + TDD prompt
    │     → Reviewer (session B, 独立 session, 同工位)
    │     → 返回 verdict + reasons
    │
    ├─ fail → Worker 改 → commit
    │   round=2: ACP session/prompt（只审增量）
    │   ...循环直到 pass...
    │
    ├─ >3轮 fail → escalate Manager 裁定
    │
    └─ pass → 写 review doc → commit → push
```

## 关键实现
- ACP session 管理: 同工位不同 session, round1 session/new, round2+ session/prompt
- A2A/SSE 反馈: Reviewer 输出 via SSE → Worker 解析
- 超过 3 轮未 pass → escalate 到 Manager
- tool: 先全部用 claude-apikey-ds-pro-auto，后续改 slot 即可

## 改动
- `bin/pr-review-guarded`
