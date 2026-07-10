---
local_id: raw-20260710T061534Z
kind: raw
phase_state: proposed
platform_ids:
  github:
    issue_id: '3867'
    url: https://github.com/chatterzhao/freely/issues/3867
    synced_at: ''
  gitee:
    issue_id: IK054H
    url: https://gitee.com/zhaoquan/freely/issues/IK054H
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-10T06:15:57Z'
updated_at: '2026-07-10T06:15:57Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## 问题

agent-roles.toml (ACP agent card)、agent-*.md (prompt 注入)、实际 A2A 委派链路三者不一致：

1. agent-roles.toml: Manager 只注册 4 skills，Worker 5，Reviewer 2
2. manager-agent.md: 列出 15 skills + CLI 命令，但 agent card 只暴露 4 个
3. ACP session/prompt 干预机制已实现但 Manager 不用
4. A2A submitted→working→completed 流程存在但 Manager 不委派

## 修复

### 1. agent-roles.toml: 补全 Manager 的 operational skills
- worktree-maintenance-governance (wt-close)
- worktree-hygiene-supervision
- multi-worktree-supervision
- doc-B1_IBM-execution, doc-B2_IBM-execution (Manager 需要理解产出)
- human-interruption-manager-triage (插话路由)

### 2. manager-agent.md: 重构 Role Definition
- 前置: 身份 (我是项目主人) + 可用 Agent (Worker/Reviewer) + 通信协议 (ACP session/prompt + A2A)
- 中置: 巡逻流程 (简化, 强调 scan → 决策 → 委派)
- 后置: 工具速查 (与 agent-roles.toml 对齐)

### 3. Worker/Reviewer agent 分工明确化
- 明确 Manager→Worker 委派协议: A2A submitted → working → completed
- 明确 Manager→Reviewer 审查触发: Worker input-required(needs-review) → SSE → Reviewer

## 验收
- Manager 收到 scan 后能自主决定开工位 + 委派 Worker
- Worker 完成后 Manager 自动收到通知并收口
