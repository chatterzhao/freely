---
local_id: I-20260321-0257
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '32'
    url: https://github.com/chatterzhao/freely/issues/32
    synced_at: '2026-04-27T11:14:53Z'
  gitee:
    issue_id: IJFO5S
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5S
    synced_at: '2026-04-27T13:14:25Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/git-worktree/worktree-fleet-governance-closure/issues/worktree-fleet-governance-closure.md
last_synced_comment_at:
  github: '2026-04-27T11:14:53Z'
hash: ''
created_at: '2026-04-27T11:14:53Z'
updated_at: '2026-04-27T11:14:53Z'
platform_state: closed
---

Freely 已经具备单树 worktree audit、merge-prep、stacked merge-chain 和 retirement handoff，但还缺一层“项目级 fleet closure”。

这会让主管在面对大量 active worktree 时只能临时拼：

- `git worktree list`
- `wt-status-all`
- pre-brainstorm / candidate / milestone / issue
- review / tests / implementation reality
- 是否已 merge / 是否该 cleanup

结果是：

- 有些树其实只该继续开发，不该强行关闭
- 有些树已可向上 merge，却没人把它纳入统一 closure plan
- 有些树已经 merge 但未 cleanup，治理未真正结束
- 有些树 candidate / issue 生命周期未闭环，却容易被误判为“完成”

canonical: docs/B2-docs/git-worktree/worktree-fleet-governance-closure/issues/worktree-fleet-governance-closure.md
