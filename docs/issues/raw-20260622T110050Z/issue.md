---
local_id: raw-20260622T110050Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260622T110050Z-A
platform_ids:
  github:
    issue_id: '3351'
    url: https://github.com/chatterzhao/freely/issues/3351
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-22T11:01:06Z'
updated_at: '2026-06-22T11:01:06Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## 问题

当前 wt-close 遇到 phase_state != completed 时只报：

```
Error: raw-xxx phase_state="absorbed", not "completed"
  Use --force to skip this check.
```

这直接引导用户用 --force 绕过，而不是先判断状态为什么不匹配。

## 改进

错误提示改为三路引导：

1. 实现已完成，只是 phase_state 忘记更新 → 更新状态后重新 wt-close
2. 实现确实还没做完 → 继续工作
3. 功能已放弃 → 使用 --force + --reason 给出业务理由

同样修复 pretests-retirement-gate 的错误提示。

## 涉及文件

- `docs/system/workspace/scripts/worktree/wt-close` — Phase 1 Checks 部分

🤖 Generated with [Claude Code](https://claude.com/claude-code)
