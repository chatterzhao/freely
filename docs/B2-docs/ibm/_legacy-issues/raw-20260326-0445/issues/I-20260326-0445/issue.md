---
local_id: I-20260326-0445
kind: linked
phase_state: dropped
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260326-0445/code-reviews
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '55'
    url: https://github.com/chatterzhao/freely/issues/55
    synced_at: '2026-04-27T11:17:21Z'
  gitee:
    issue_id: IJFO6O
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6O
    synced_at: '2026-04-27T13:14:58Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/manager-delegated-intake-absorption-closure-governance/issues/manager-delegated-intake-absorption-closure-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:17:21Z'
hash: ''
created_at: '2026-04-27T11:17:21Z'
updated_at: '2026-04-27T11:17:21Z'
platform_state: closed
---

Freely 已经解决了 manager delegated continuation 的：

- intake durability
- classification / delegation
- prompt-level consumed evidence
- live-status pending-vs-consumed 可见性

但真实 dogfood 证明当前还缺最终 lifecycle closure：

- manager continuity 会把旧 interruption 一再写入 `absorbed_intake_ids`
- session-state / live-status 会把同一批 delegated continuation 记为 consumed
- 对应 `.freely/intake/<id>/meta.env` 却长期停在 `STATUS="delegated"`

这样会制造两个坏结果：

1. machine-readable backlog 会无限积灰，主管必须不断解释“这些其实已经 absorb 过”；
2. manager judg

canonical: docs/B2-docs/ibm/manager-delegated-intake-absorption-closure-governance/issues/manager-delegated-intake-absorption-closure-governance.md
