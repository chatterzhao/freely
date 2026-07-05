---
local_id: I-20260320-1405
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '28'
    url: https://github.com/chatterzhao/freely/issues/28
    synced_at: '2026-04-27T11:14:31Z'
  gitee:
    issue_id: IJFO5O
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5O
    synced_at: '2026-04-27T13:14:19Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/git-worktree/worktree-maintenance-governance/issues/worktree-maintenance-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:14:31Z'
hash: ''
created_at: '2026-04-27T11:14:31Z'
updated_at: '2026-04-27T11:14:31Z'
platform_state: closed
---

Freely 现有技能已经覆盖：

- how to create worktrees
- how to watch dirty/checkpoint/runtime state
- how to cleanup after verified retirement

但没有一条能力专门负责 worktree 创建后的维护：

- 单棵树真实状态审计
- 多棵树 merge-prep 顺序与冲突面
- companion / obsolete worktree 的 salvage_then_retire

这会让主管在 worktree 积累后反复用 milestone、issue、review、tests、git ancestry 和聊天上下文临时拼判断。

canonical: docs/B2-docs/git-worktree/worktree-maintenance-governance/issues/worktree-maintenance-governance.md
