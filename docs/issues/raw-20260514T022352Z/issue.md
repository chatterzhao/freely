---
local_id: raw-20260514T022352Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260514T022352Z-A
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: '2026-06-17T00:25:36Z'
platform_ids:
  github:
    issue_id: '341'
    url: https://github.com/chatterzhao/freely/issues/341
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-14T02:24:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-14T02:50:24Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## raw-20260514T022352Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260514T022352Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-14T02:23:52Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260514T022352Z`。实现前请用 `wt-create --raw-key 20260514T022352Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-14T02:23:52Z"
title: "cleanup: remove remaining hardcoded alias cc-ds-auto from start-lead-agent.sh, freely, monitor-ai-cli.sh"

cc-ds-auto 的 alias 是 `claude --settings ...`（裸二进制开头），通用 `_resolve_tool_family` 路径已能正确处理。三处硬编码是历史残留，应删除。

| 文件 | 行 | 删除 |
|------|-----|------|
| docs/system/workspace/scripts/start-lead-agent.sh | 215 | 从 case 列表移除 cc-ds-auto |
| docs/system/workspace/scripts/runtime/freely | 17505 | 从 case 列表移除 cc-ds-auto |
| docs/system/workspace/scripts/monitor-ai-cli.sh | 101 | 从 case 列表移除 cc-ds-auto |
