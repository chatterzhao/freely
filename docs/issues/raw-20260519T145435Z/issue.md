---
local_id: raw-20260519T145435Z
kind: raw
phase_state: dropped
phase_state: absorbed
platform_ids:
  github:
    issue_id: '655'
    url: https://github.com/chatterzhao/freely/issues/655
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-19T14:54:52Z'
updated_at: '2026-05-19T14:54:52Z'
intake_id: ''
author: platform
channel: github
session_refs: []
dropped_reason: Fix merged directly to develop via pr-merge-guarded. Runtime bug fix
  does not warrant full B1→I-* chain.
---

## raw-20260519T145435Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260519T145435Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-05-19T14:54:35Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260519T145435Z`。实现前请用 `wt-create --raw-key 20260519T145435Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
phase_state: absorbed
source: feedback
created_at: "2026-05-19T14:54:35Z"
title: "consumed_by routing field + auto_consume premature consumption design fix"

## 问题

1. worker handoff 的 `consumed_by` 被错误设为 `worker`，应为 `manager`（Manager 是 worker 汇报的消费者）
2. `auto_consume` 在 Manager runtime 处理 handoff 时过早执行，在 Manager 还没读取 worker 汇报前就把 `status` 改为 `consumed`
3. Manager prompt 过滤 `status != 'consumed'`，导致 Manager 看不到任何 worker 汇报

## 修复

1. `consumed_by`: worker INSERT 时从 `worker` 改为 `manager`
2. `auto_consume`: 从 Manager runtime（`_manager_auto_consume_workers`）移到 `wt-close`（工位关闭时）
3. wt-close Phase 5 前执行 auto_consume，按 branch 名提取 raw_key

## 设计原则

- `consumed_by` = 路由字段，指定谁应消费（INSERT 时设置，不改变）
- `status='consumed'` = 已消费标志（消费后设置）
- 消费者应在工位关闭后消费，而非 Manager 产出新 handoff 时提前消费
