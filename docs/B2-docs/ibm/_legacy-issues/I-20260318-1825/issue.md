---
local_id: I-20260318-1825
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '20'
    url: https://github.com/chatterzhao/freely/issues/20
    synced_at: '2026-04-27T11:13:54Z'
  gitee:
    issue_id: IJFO5E
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5E
    synced_at: '2026-04-27T13:14:04Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/git-worktree/worktree-hygiene-supervision-control-plane/issues/worktree-hygiene-supervision-control-plane.md
last_synced_comment_at:
  github: '2026-04-27T11:13:54Z'
hash: ''
created_at: '2026-04-27T11:13:54Z'
updated_at: '2026-04-27T11:13:54Z'
platform_state: closed
---

Freely 已有 checkpoint-guard、fleet-status 与 manager/worker 角色边界，但还缺一条更主动的自治控制面：

- worker 连续多轮 dirty/checkpoint 漂移时，runtime 只会提醒，不会升级为明确的 hygiene intervention
- manager 能看到 dirty/checkpoint 数字，但缺少可直接委派的 hygiene alert
- 缺少一个统一的 hygiene skill，把 manager 的委派和 worker 的收口步骤收成同源能力

canonical: docs/B2-docs/git-worktree/worktree-hygiene-supervision-control-plane/issues/worktree-hygiene-supervision-control-plane.md
