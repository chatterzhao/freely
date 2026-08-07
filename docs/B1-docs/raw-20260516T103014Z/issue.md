---
local_id: raw-20260516T103014Z14Z
kind: raw
- phase_state: dropped
closeout_note: 平台 issue 已关闭，本地 lifecycle 标记完成（batch round7）
updated_at: 2026-05-17 04:47:25+00:00
platform_ids:
  github:
    issue_id: '367'
    url: https://github.com/chatterzhao/freely/issues/367
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-16T10:30:28Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
force_closed_at: '2026-05-16T10:33:23Z'
force_closed_reason: 'wt-close --force: worktree retired without completed phase_state'
---

## raw-20260516T103014Z14Z

| Field | Value |
|-------|-------|
| local_id | `raw-20260516T103014Z14Z` |
| kind | `raw` |
| status | `open` |
| phase | `none` |
| canonical | `none` |
| created | 2026-05-16T10:30:14Z |
| updated | unknown |

---

> **Freely 治理**：这是 raw issue `raw-20260516T103014Z14Z`。实现前请用 `wt-create --raw-key 20260516T103014Z` 创建专属工位，确保代码修改在包含此 raw-key 的分支上进行。
kind: raw
priority: P2
status: open
source: chat-inbox
created_at: "2026-05-16T10:30:14Z"
title: "run-acp-prompt.py: stop_reason 在 finally 块中未初始化就被引用，掩盖真正异常"

## 根因

`run-acp-prompt.py` 的 main 逻辑：

```python
try:                                    # 322
    ...
    stop_reason = send_prompt(...)      # 461 ← 赋值点
    ...
finally:                                # 488
    if stop_reason == "end_turn":       # 489 ← 未初始化就引用！
```

如果 try 块在 461 行之前抛出任何异常，`stop_reason` 从未被赋值，finally 块执行到 489 行时触发 `UnboundLocalError: local variable 'stop_reason' referenced before assignment`。

这个错误掩盖了真正的异常原因（session/prompt 为什么失败），导致 cycle log 只能看到 `[ERROR] local variable 'stop_reason' referenced before assignment`。

## 修复

在 `try:` 之前初始化 `stop_reason = "error"`。这样 finally 块不会崩溃，原始异常也能被正确报告。

```python
stop_reason = "error"  # 新增：防止 finally 块 UnboundLocalError
try:
    ...
    stop_reason = send_prompt(...)
    ...
finally:
    if stop_reason == "end_turn":  # 现在安全了
```

## 影响

AI cycle 返回 rc=1，runtime 无法区分"stop_reason 变量 bug"和"真正的 prompt 失败"。
