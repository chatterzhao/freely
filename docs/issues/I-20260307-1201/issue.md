---
local_id: I-20260307-1201
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '13'
    url: https://github.com/chatterzhao/freely/issues/13
    synced_at: '2026-04-27T11:13:15Z'
  gitee:
    issue_id: IJFO4C
    url: https://gitee.com/zhaoquan/freely/issues/IJFO4C
    synced_at: '2026-04-27T13:13:09Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/issues/source-routing-and-derived-worktree-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:13:15Z'
hash: ''
created_at: '2026-04-27T11:13:15Z'
updated_at: '2026-04-27T11:13:15Z'
platform_state: closed
---

收紧 Freely 自举时的整体路由逻辑，确保：
- 问题来源分层清晰
- candidate 必须进入 milestone 后再进入 IBM
- `IBM` 只处理 milestone-owned issue
- `progress` 只跟踪 dev-loop 执行态
- 依赖未合并父分支的子任务可以使用 derived worktree
- skill 以情景步骤而不是抽象约束来指导 AI 执行
- 首跳在同工具场景下必须继续执行第二跳，而不是把 `next_prompt` 当作终点

canonical: docs/epics/workspace-routing-foundation/source-routing-and-derived-worktree-governance/issues/source-routing-and-derived-worktree-governance.md
