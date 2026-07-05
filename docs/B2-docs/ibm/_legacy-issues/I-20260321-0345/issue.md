---
local_id: I-20260321-0345
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '33'
    url: https://github.com/chatterzhao/freely/issues/33
    synced_at: '2026-04-27T11:15:02Z'
  gitee:
    issue_id: IJFO5U
    url: https://gitee.com/zhaoquan/freely/issues/IJFO5U
    synced_at: '2026-04-27T13:14:26Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/manager-reactivation-and-fleet-patrol-governance/issues/manager-reactivation-and-fleet-patrol-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:15:02Z'
hash: ''
created_at: '2026-04-27T11:15:02Z'
updated_at: '2026-04-27T11:15:02Z'
platform_state: closed
---

Freely 现在已经能通过 runtime watchdog 拉起主管，也能通过 `live-status` / `fleet-status` / worktree skills 观察当前项目状态。

但还缺一条更明确的主管 patrol 协议：

- 主管重激活后，要先巡检整个 fleet，而不是只等下一条 event source
- 主管需要主动发现“哪些 phase / issue / worktree 当前没有 worker 推进”
- 主管需要主动发现“issue 已完成但 worktree 未收口”

否则 Freely 只能做到：
- manager process alive

做不到：
- manager actually supervising the fleet

canonical: docs/B2-docs/ibm/manager-reactivation-and-fleet-patrol-governance/issues/manager-reactivation-and-fleet-patrol-governance.md
