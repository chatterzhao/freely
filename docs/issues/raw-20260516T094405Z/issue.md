---
kind: raw
local_id: raw-20260516T094405Z
priority: P2
phase_state: dropped
source: chat-inbox
created_at: '2026-05-16T09:44:05Z'
title: delegate_workers 被 exclusive_fields_conflict 拒绝：reason 字段被误当作 stop_reason
platform_ids:
  github:
    issue_id: '363'
    url: https://github.com/chatterzhao/freely/issues/363
    synced_at: '2026-05-16T09:44:11Z'
updated_at: '2026-05-26T12:31:10Z'
primary_platform: github
platform_state: closed
force_closed_at: '2026-05-16T09:48:58Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## 根因

`validate_manager_exit_contract_for_project` 行 13536：
```bash
stop_reason="$(_db_exit_contract_field "$project" manager reason)"
```

将 DB 的 `reason` 字段无条件读入 `stop_reason` 变量。然后在行 13559：
```bash
[[ -z "$stop_reason$restart_point$next_action$why_not_stop$why_not_delegate" ]] \
  || missing_csv="exclusive_fields_conflict"
```

对 `delegate_workers`，`reason` 是合法字段（Manager 解释委派原因），但因为被赋值给了 `stop_reason`，`$stop_reason` 非空 → `exclusive_fields_conflict`。

## 修复

`stop_reason` 应该只在 `exit_kind=stop_ai` 时读取，或者用一个独立变量名（如 `_reason`），`stop_reason` 只用于 stop_ai 的排他性检查。

## 影响

Manager 每次 delegate_workers 都被拒绝，worker 永远不启动。
