---
local_id: raw-20260519T175836Z
kind: raw
phase_state: dropped
platform_ids:
  github:
    issue_id: '661'
    url: https://github.com/chatterzhao/freely/issues/661
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-19T17:58:50Z'
updated_at: '2026-05-26T12:28:20Z'
intake_id: ''
author: platform
channel: github
session_refs: []
dropped_reason: Implementation merged to develop. send_to_ai field + ACP prompt mode
  + build_prompt delta mode.
platform_state: closed
force_closed_at: '2026-05-19T22:49:06Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## raw-20260519T175836Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260519T175836Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-05-19T17:58:36Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260519T175836Z`。实现前请用 `wt-create --raw-key 20260519T175836Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
phase_state: proposed
source: feedback
created_at: "2026-05-19T17:58:36Z"
title: "handoffs 读写分离：Agent 只写，Runtime 管路由和送达"

## 设计

handoffs 表是 agent 间消息传递系统。职责分离：

| 角色 | 职责 |
|------|------|
| Manager/Worker | 只写 handoff（exit_kind + reason + completion_summary 等） |
| Runtime | 读 handoffs，查 send_to_ai=pending/fail，组装 prompt，发给 consumed_by |

Agent 永远不需要查 handoffs 表——需要的信息已在 prompt 里。

## 改动

1. 新增字段 ：pending（未送达）/ success（已送达）/ fail（送达失败）
2. Runtime 组 prompt 时查 ，注入对应 consumed_by 的 prompt
3.  成功后 UPDATE 
4. 去掉  状态—— 即已送达
5. 保留  作路由字段
6.  评估：pending→launched→completed/blocked/rejected 可能仍需要（worker 任务进度），但可简化

## 流程
