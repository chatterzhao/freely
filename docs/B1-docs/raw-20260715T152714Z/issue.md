---
local_id: raw-20260715T152714Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '3918'
    url: https://github.com/chatterzhao/freely/issues/3918
    synced_at: ''
  gitee:
    issue_id: IK1BCG
    url: https://gitee.com/zhaoquan/freely/issues/IK1BCG
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-15T15:27:39Z'
updated_at: '2026-07-15T15:27:39Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

\n\n## 根因

daemon 启动后 Manager prompt 只注入 scan 数据（task-lifecycle-scan），没有当前进行中的工作进度上下文。Manager 看到活跃工位和 stale A2A tasks 时无从判断哪些是"进行中应继续"还是"残留应清理"，导致错误地将进行中的工位委派标记为 completed。

## 设计

prompt 注入优先级：
1. Recovery context（agent_working 表 + git worktree list + A2A tasks）—— 进行中的工作
2. Scan data —— 待处理的新任务

Recovery context 从以下来源组装：
- agent_working 表：活跃 agent、工位路径、slot、session
- git worktree list：实际存在的工位
- A2A tasks：委派状态（submitted/working/input-required）
- milestones.md：各 raw issue 的 phase_state

注入格式：简洁的结构化摘要，优先级高于 scan。让 Manager 能判断"继续推进"vs"清理收口"。

## 影响
Manager 重启后能正确恢复上下文，继续推进进行中的工位而非当作垃圾清理。
