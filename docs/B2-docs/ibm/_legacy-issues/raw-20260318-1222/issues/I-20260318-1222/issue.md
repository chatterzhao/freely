---
local_id: I-20260318-1222
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260318-1222/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '16'
    url: https://github.com/chatterzhao/freely/issues/16
    synced_at: '2026-04-27T11:13:28Z'
  gitee:
    issue_id: IJFO55
    url: https://gitee.com/zhaoquan/freely/issues/IJFO55
    synced_at: '2026-04-27T13:13:58Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/mem9-continuity-bridge/issues/mem9-continuity-bridge.md
last_synced_comment_at:
  github: '2026-04-27T11:13:28Z'
hash: ''
created_at: '2026-04-27T11:13:28Z'
updated_at: '2026-04-27T11:13:28Z'
platform_state: closed
---

Freely 已经拥有本地 continuity / recovery / session rotation / multi-worktree supervision，但还没有一个正式的外部共享记忆边界来回答：

- 什么可以写入外部 memory backend
- 什么必须继续由本地治理事实源裁决
- 外部 memory 是否只作为 continuity enhancement，而不是 authority

canonical: docs/B2-docs/ibm/mem9-continuity-bridge/issues/mem9-continuity-bridge.md
