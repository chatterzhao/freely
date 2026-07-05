---
local_id: I-20260321-1515
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '35'
    url: https://github.com/chatterzhao/freely/issues/35
    synced_at: '2026-04-27T11:15:17Z'
  gitee:
    issue_id: IJFO5X
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5X
    synced_at: '2026-04-27T13:14:29Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/remote-branch-retirement-governance/issues/remote-branch-retirement-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:15:17Z'
hash: ''
created_at: '2026-04-27T11:15:17Z'
updated_at: '2026-04-27T11:15:17Z'
platform_state: closed
---

Freely 当前已经能：

- merge up 到 `develop`
- 删除本地 worktree
- 删除本地 feature branch

但 worktree 治理真正完成时，远程同名 branch 也必须进入明确 disposition：

- deleted
- retained with reason

否则治理闭环会停在“本地看起来已经退休”，而远程协作面仍保留历史 feature branch。

canonical: docs/epics/workspace-routing-foundation/remote-branch-retirement-governance/issues/remote-branch-retirement-governance.md
