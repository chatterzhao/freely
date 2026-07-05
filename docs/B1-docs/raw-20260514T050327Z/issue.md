---
local_id: raw-20260514T050327Z
kind: raw
phase_state: completed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '342'
    url: https://github.com/chatterzhao/freely/issues/342
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-14T05:03:40Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

## raw-20260514T050327Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260514T050327Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-14T05:03:27Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260514T050327Z`。实现前请用 `wt-create --raw-key 20260514T050327Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P1
status: open
source: chat-inbox
created_at: "2026-05-14T05:03:27Z"
title: "fix: tool-launchers.sh _apply_tool_alias_settings while/then typo causes syntax error"

## Root cause

In `_apply_tool_alias_settings()`, line 309:
```bash
while [[ "$remainder" =~ ^[[:space:]]*([a-zA-Z_][a-zA-Z0-9_]*)= ]]; then
```

`then` should be `do`. `while` loops in bash use `do...done`, not `then`.

## Impact

`_apply_tool_alias_settings` fails with syntax error on every ACP launch via alias.
`run-acp-prompt.py` exits with rc=2 because tool-launchers.sh can't parse.
The env prefix export never runs, so OPENCODE_CONFIG is never set.

## Fix

`s/then/do/` at line 309 of docs/system/workspace/scripts/runtime/tool-launchers.sh

Introduced in commit 85083851 (generalize alias resolution).
