---
local_id: raw-20260519T155813Z
kind: raw
phase_state: dropped
platform_ids:
  github:
    issue_id: '659'
    url: https://github.com/chatterzhao/freely/issues/659
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-19T15:58:28Z'
updated_at: '2026-05-27T00:11:31Z'
intake_id: ''
author: platform
channel: github
session_refs: []
dropped_reason: Fix merged to develop via fix/raw-20260519T155813Z-launchable-reason.
  Runtime bug fix.
platform_state: closed
---

## raw-20260519T155813Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260519T155813Z` |
| kind | `raw` |
| phase_state | `proposed` |
| canonical | `none` |
| created | 2026-05-19T15:58:13Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260519T155813Z`。实现前请用 `wt-create --raw-key 20260519T155813Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
phase_state: proposed
source: feedback
created_at: "2026-05-19T15:58:13Z"
title: "launchable check failed reason too vague — need actionable rejection messages"

## 问题

`worker_prompt_launchable_for_manager_project` 多个失败路径没有设置 `LAUNCH_REJECT_REASON`，fallback 为 `launchable check failed`，Manager 无法根据原因修复。

具体缺失：
1. worktree 不存在 → 无 reason
2. worktree 有 followthrough prompt → 无 reason  
3. absorbed/merged lane 非 cleanup → 无 reason
4. develop cleanup（理论允许但实际不应允许）→ 无 reason

## 修复

每个 return 1 前设置清晰的 `LAUNCH_REJECT_REASON`，包含：
- 为什么失败
- 建议的修复命令（wt-create --raw-key <key> ...）
- 具体的 actionable 信息

## 影响

Manager 看到 launch_failed worker 后能根据 reason 采取正确行动（创建工位、换个分支等），而不是连续 stop_ai。
