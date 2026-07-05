---
local_id: I-20260322-0412
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '48'
    url: https://github.com/chatterzhao/freely/issues/48
    synced_at: '2026-04-27T11:16:42Z'
  gitee:
    issue_id: IJFO6G
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6G
    synced_at: '2026-04-27T13:14:48Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/worker-active-reentry-for-manager-delegated-continuation-governance/issues/worker-active-reentry-for-manager-delegated-continuation-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:16:42Z'
hash: ''
created_at: '2026-04-27T11:16:42Z'
updated_at: '2026-04-27T11:16:42Z'
platform_state: closed
---

manager runtime 已经能把 stable worker prompt 转成目标 worker worktree 的 delegated continuation intake，并拉起 worker runtime。但当目标 worker 已经有 active AI 时，这条 delegated continuation 不会被及时消费，导致“worker 已活着，但 handoff 没真正进入下一轮”。

canonical: docs/B2-docs/ibm/worker-active-reentry-for-manager-delegated-continuation-governance/issues/worker-active-reentry-for-manager-delegated-continuation-governance.md
