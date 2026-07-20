---
local_id: raw-20260506T010000Z00Z
kind: raw
phase_state: absorbed
absorbed_into: docs/B2-docs/ibm/_legacy-issues/raw-20260506T1000Z/issues/I-20260506T1000Z-A/issue.md
platform_ids:
  github:
    issue_id: '231'
    url: https://github.com/chatterzhao/freely/issues/231
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-06T17:49:23Z'
updated_at: '2026-05-19T22:48:21Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-19T22:48:21Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## raw-20260506T010000Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260506T010000Z` |
| kind | `raw` |
| status | `unknown` |
| phase | `proposed` |
| canonical | `none` |
| created | 2026-05-06 10:00:00+00:00 |
| updated | 2026-05-06 10:00:00+00:00 |

---

local_id: raw-20260506T010000Z00Z
kind: raw
phase_state: proposed
platform_ids:
  github: "229"
primary_platform: github
canonical_issue_path: ""
last_synced_comment_at: {}
hash: ""
created_at: 2026-05-06T10:00:00Z
updated_at: 2026-05-06T10:00:00Z
intake_id: ""
author: zhaoquan
channel: github
session_refs: []
platform_state: ''

## 问题

`task_mode=wait` 启动 Freely 时仍会发射 AI 循环。门禁仅存在于 AI 结束后的 `manager_runtime_handle_exit_contract_after_ai_cycle`（stop_ai handler），缺少 supervisor 循环在 build prompt / launch AI 之前的前置轮询门禁。

## 预期行为

wait 模式 supervisor 不 build prompt、不 launch AI，仅轮询 task_mode_gate 直到用户通过 `task-mode set` 切换为 auto 或 id:<scan-id>。

## 根因

原始 `task-mode gate` 实现 (32243539) 将 wait 门禁仅放在 stop_ai 后置处理器中。sleep CHECK_INTERVAL 后返回 continue，使 supervisor 回到主循环再次 build prompt + launch AI。

## 修复方案

Supervisor 主循环 `select_launch_kind` 前增加 manager 专属前置门禁：`read_task_mode=wait` → `sleep CHECK_INTERVAL` → `continue`。
