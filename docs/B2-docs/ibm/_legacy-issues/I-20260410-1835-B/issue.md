---
local_id: I-20260410-1835-B
kind: linked
phase_state: completed
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '132'
    url: https://github.com/chatterzhao/freely/issues/132
    synced_at: '2026-04-27T11:26:33Z'
  gitee:
    issue_id: IJFO9H
    url: https://gitee.com/zhaoquan/freely/issues/IJFO9H
    synced_at: '2026-04-27T13:16:59Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/codex-real-exec-switch-and-after-failure-recovery-governance/issues/codex-real-exec-switch-and-after-failure-recovery-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:26:33Z'
hash: ''
created_at: '2026-04-27T11:26:33Z'
updated_at: '2026-05-17T08:01:59Z'
platform_state: closed
---

Real dogfooding on 2026-04-12 exposed a narrower follow-on regression in the already completed Codex recovery family:

1. `codex exec "hi"` probe success was too weak and could still produce false positives
2. runtime failure classification still let reconnect-plus-403/quota evidence fall into `execution_network_*`, which kept the bad current slot alive instead of moving forward

This is not a new generic network-taxonomy owner. It is a bounded closeout of the specific mismatch between real `hi`

canonical: docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/issues/codex-probe-success-shape-and-quota-slot-recovery-governance.md
