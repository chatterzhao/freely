---
local_id: raw-20260516T095920Z
kind: raw
phase_state: dropped
updated_at: '2026-05-31T00:30:00Z'
closeout_note: fix directly merged to develop via fix/raw-20260512T0915Z-worker-blocked-reason
  without I-* lifecycle chain
platform_ids:
  github:
    issue_id: '365'
    url: https://github.com/chatterzhao/freely/issues/365
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T09:59:34Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## raw-20260516T095920Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T095920Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T09:59:20Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T095920Z`。实现前请用 `wt-create --raw-key 20260516T095920Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-16T09:59:20Z"
title: "worker validate_worker_exit_contract 残留旧 reason 字段名，三个 exit_kind 排他性检查全坏"

## 背景

#344 将 handoffs 表的 `stop_reason`/`blocked_reason`/`handoff_reason` 统一为单个 `reason` 字段。
Manager 侧已在 #363 + #364 修复。Worker 侧仍有相同问题。

## 当前遗漏（行 13679-13712）

```bash
blocked_reason="$(_db_exit_contract_field "$project" worker reason)"   # 13694
handoff_reason="$(_db_exit_contract_field "$project" worker reason)"   # 13695
```

两个变量读同一个 `reason` 值 → 排他性检查全部失效。

| exit_kind | 排他检查 | 实际效果 |
|-----------|---------|---------|
| worker_done | `$blocked_reason$handoff_reason$next_action` 应为空 | 两个都非空 → 拒绝 |
| worker_blocked | `$completion_summary$evidence_paths$handoff_reason` 应为空 | `handoff_reason` 非空 → 拒绝 |
| worker_handoff_needed | `$completion_summary$evidence_paths$blocked_reason` 应为空 | `blocked_reason` 非空 → 拒绝 |

同时 worker_blocked 要求 `blocked_reason` 非空（13704），worker_handoff_needed 要求 `handoff_reason` 非空（13709）。
因为两个都指向 reason，只要 Worker 填了 reason 就两个都"满足"——语义全错。

## 修复方案

与 #364 相同策略：
- 旧字段 `blocked_reason`/`handoff_reason` 设为空字符串
- 用统一的 `_worker_reason` 读 `reason` 字段
- 排他检查移除旧的字段名
- `worker_blocked` 和 `worker_handoff_needed` 的必填检查不再依赖旧字段名（两个 exit_kind 共用 reason 是合法的）

## 范围

`docs/system/workspace/scripts/runtime/freely` 中 `validate_worker_exit_contract_for_project` 函数。
