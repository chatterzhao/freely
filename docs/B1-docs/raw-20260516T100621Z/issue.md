---
local_id: raw-20260516T100621Z21Z
kind: raw
phase_state: absorbed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '366'
    url: https://github.com/chatterzhao/freely/issues/366
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T10:06:39Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-16T10:12:49Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
absorbed_into: raw-20260710T005219Z---

## consume_delegate_workers (13979-14033)

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T100621Z21Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T10:06:21Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T100621Z21Z`。实现前请用 `wt-create --raw-key 20260516T100621Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-16T10:06:21Z"
title: "reason 字段统一后残留问题：resume_reason 变量引用错误，event 日志用旧字段名"

## 审计结果

#344 将 `stop_reason`/`blocked_reason`/`handoff_reason`/`why_not_stop`/`why_not_delegate` 统一为 `reason`。经 #363/#364/#365 修复，排他性检查已全部修正。但仍有以下残留：

### 1. Bug：line 13774 引用了未定义变量

```bash
resume_reason="$(_db_exit_contract_field "$project" manager reason)"  # 13764
...
- reason: ${reason:-manager_exit_contract_resume}  # 13774 ← $reason 未定义！
- reason: ${resume_reason:-unknown}                # 13780 ← 正确
```

13774 的 `${reason}` 永远不会被设置，始终 fallback 到 `manager_exit_contract_resume`。应为 `${resume_reason}`。

### 2. Event 日志用旧字段名（不影响功能，但误导）

```bash
# consume_delegate_workers (13979-14033)
stop_reason="$(_db_exit_contract_field "$project" manager reason)"  # 读的是 reason

# worker event 记录 (14164-14171)
"blocked_reason=$(_db_exit_contract_field "$project" worker reason)"
"handoff_reason=$(_db_exit_contract_field "$project" worker reason)"
```

这些都是日志/事件输出，不影响行为。但读的是 `reason` 却命名为旧字段名，混淆了排错。

### 3. 验证逻辑的变量命名（已修复功能，命名可优化）

| 行 | 变量 | 读的列 | 用途 | 状态 |
|----|------|--------|------|------|
| 13536 | `stop_reason` | `reason` | stop_ai 必填检查 | ✅ 功能正确 |
| 13694 | `blocked_reason` | `reason` | worker_blocked 必填检查 | ✅ 功能正确 |
| 13695 | `handoff_reason` | `reason` | worker_handoff_needed 必填检查 | ✅ 功能正确 |
| 13979 | `stop_reason` | `reason` | delegate event 日志 | ⚠️ 命名误导 |

## 修复建议

1. **修 bug**：13774 `${reason}` → `${resume_reason}`
2. **统一命名**（低优先级）：将所有 `stop_reason`/`blocked_reason`/`handoff_reason` 局部变量统一为 `_manager_reason` / `_worker_reason`，使代码与 schema 一致
