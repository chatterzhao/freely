---
local_id: I-20260412-0907-A
kind: linked
phase_state: completed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260412-0907/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '139'
    url: https://github.com/chatterzhao/freely/issues/139
    synced_at: '2026-04-27T11:26:53Z'
  gitee:
    issue_id: IJFO9Q
    url: https://gitee.com/zhaoquan/freely/issues/IJFO9Q
    synced_at: '2026-04-27T13:17:08Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/raw-20260412-0907issues/codex-probe-success-shape-and-quota-slot-recovery-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:26:53Z'
hash: ''
created_at: '2026-04-27T11:26:53Z'
updated_at: '2026-05-17T12:24:13Z'
platform_state: closed
---

Real dogfooding on 2026-04-12 exposed a narrower follow-on regression in the already completed Codex recovery family:

1. `codex exec "hi"` probe success was too weak and could still produce false positives
2. runtime failure classification still let reconnect-plus-403/quota evidence fall into `execution_network_*`, which kept the bad current slot alive instead of moving forward

This is not a new generic network-taxonomy owner. It is a bounded closeout of the specific mismatch between real `hi`

canonical: docs/B2-docs/config/codex-probe-success-shape-and-quota-slot-recovery-governance/raw-20260412-0907issues/codex-probe-success-shape-and-quota-slot-recovery-governance.md
