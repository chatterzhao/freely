---
local_id: raw-20260516T081651Z
kind: raw
phase_state: completed
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17T04:47:25Z
platform_ids:
  github:
    issue_id: '360'
    url: https://github.com/chatterzhao/freely/issues/360
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T08:17:04Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-16T08:19:52Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## raw-20260516T081651Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T081651Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T08:16:51Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T081651Z`。实现前请用 `wt-create --raw-key 20260516T081651Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-16T08:16:51Z"
title: "handoff JSON 解析失败：stop_reason=end_turn 紧贴 ``` 导致正则匹配失败"

## 根因

`run-acp-prompt.py` 的 `send_prompt()` 通过 `sys.stdout.write(chunk_text)` 输出 AI 响应文本（无尾随换行），然后 `print(f\"stop_reason={stop_reason}\")` 追加输出。

当 AI 的最后一个 chunk 以 `\`\`\`` 结尾时（handoff JSON 关闭标记），输出流变成：
```
}
```stop_reason=end_turn
```

`handoff.py:extract_handoff_block()` 的正则 `r'\`\`\`handoff\s*\n(.*?)\n\`\`\`'` 要求 `\n` 在关闭 `\`\`\`` 之前，但实际文本中 `stop_reason=end_turn` 在同一行紧贴 ``` 后面，导致正则永远返回 None。

## 修复

两处改动：

1. **`handoff.py` `extract_handoff_block()`**（主要）：正则改为 `r'\`\`\`handoff\s*\n(.*?)\n\`\`\`\S*'`，允许关闭 ``` 后面有非空白字符（如 `stop_reason=end_turn`）。这是防御性修复——handoff 解析器应对各种 AI 输出格式保持鲁棒。

2. **`run-acp-prompt.py` `send_prompt()`**（次要）：在 `print(f\"stop_reason={stop_reason}\")` 之前加一个空 `print()` 确保换行。

## 影响

- Manager 输出 `delegate_workers` handoff → runtime 解析为 `exit_kind=error` → worker 永远不启动
- Manager 陷入无效重试循环（同一 session resume，每次重新输出 handoff，每次解析失败）
