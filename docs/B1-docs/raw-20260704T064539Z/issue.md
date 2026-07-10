---
local_id: raw-20260704T064539Z39Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3726'
    url: https://github.com/chatterzhao/freely/issues/3726
    synced_at: ''
  gitee:
    issue_id: IJYRNK
    url: https://gitee.com/zhaoquan/freely/issues/IJYRNK
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-04T06:46:16Z'
updated_at: '2026-07-04T06:46:16Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n
## 问题 1: 三个角色 session 创建逻辑分散

Manager、Worker、Reviewer 各走各的 agent_assign 调用，参数不全、逻辑不一致：

| 角色 | 缺失参数 |
|------|---------|
| Manager | slot, session_id (可能空), test_worktree, test_branch |
| Worker | slot 未确认 |
| Reviewer | worktree, branch, 可能 slot |

## 问题 2: 无统一入口

session/new、session/fork、session/resume 三种创建方式，但没有统一的 agent_working 写入封装。

## 问题 3: CLAUDE_SESSION_ID_CURRENT 命名错误

这个变量存储任何 tool 的 session ID（opencode/claude/codex/cline），不应带 "CLAUDE" 前缀。应改为 TOOL_SESSION_ID_CURRENT 或类似 tool-agnostic 命名。

## 设计方向

抽象统一方法:
- acp_session_new(project, role, agent_id, slot, raw_key, worktree, branch) → 创建 session + 写 agent_working
- acp_session_fork(project, parent_role, child_role, agent_id, slot, raw_key, worktree, branch) → fork + 写
- acp_session_resume(project, session_id) → 更新 session_id
- acp_session_close(project, raw_key, role, agent_id) → 清 session_id

每个 role 差异仅在于 raw_key 来源:
- Manager: __manager__
- Worker/Reviewer: 从 worktree 的 issue 绑定提取

重命名:
- CLAUDE_SESSION_ID_CURRENT → TOOL_SESSION_ID_CURRENT
- 相关引用全局替换
absorbed_into: I-20260704T064539Z-A
