---
local_id: raw-20260516T095158Z58Z
kind: raw
phase_state: dropped
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17 04:47:25+00:00
platform_ids:
  github:
    issue_id: '364'
    url: https://github.com/chatterzhao/freely/issues/364
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T09:52:13Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-16T09:55:40Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## raw-20260516T095158Z58Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T095158Z58Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T09:51:58Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T095158Z58Z`。实现前请用 `wt-create --raw-key 20260516T095158Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-16T09:51:58Z"
title: "reason 字段统一后 validate_manager_exit_contract 残留旧字段名导致全部 exit_kind 排他性检查失效"

## 根因

#344 将 handoffs 表的多个 reason 字段（`stop_reason`、`blocked_reason`、`handoff_reason`）统一为单个 `reason`，但在 `validate_manager_exit_contract_for_project` 中：

```bash
stop_reason="$(_db_exit_contract_field "$project" manager reason)"     # 13536
why_not_stop="$(_db_exit_contract_field "$project" manager reason)"    # 13539
why_not_delegate="$(_db_exit_contract_field "$project" manager reason)" # 13540
```

三个变量全读同一个 `reason` 值。导致：

| exit_kind | 排他检查 | 实际效果 |
|-----------|---------|---------|
| stop_ai | `$why_not_stop$why_not_delegate` 应为空 | 如果 Manager 填了 reason，这两个变量非空 → 拒绝 |
| resume_manager | `$stop_reason` 应为空 | reason 非空 → 拒绝 |
| delegate_workers | `$stop_reason` 应为空 | 同上（#363 修了但 #359 没修） |

## 修复

将 `why_not_stop` 和 `why_not_delegate` 改为读独立字段（若 DB 无对应列则设为空），或将排他性检查逻辑改为匹配统一 schema：
- `stop_ai`：reason 是合法字段，不应排他；只检查 `restart_point$next_action$worker_prompts_csv`
- `resume_manager`：reason 是合法字段，不应排他；只检查 `$worker_prompts_csv`
- `delegate_workers`：reason 是合法字段，不应排他；只检查 `$restart_point$next_action`（已修但 stop_reason 读值仍有坑）

同样的问题也存在于 worker 验证（行 13695-13712，`blocked_reason`/`handoff_reason` 均指向 `reason`）。
