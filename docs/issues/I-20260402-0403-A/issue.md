---
local_id: I-20260402-0403-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '90'
    url: https://github.com/chatterzhao/freely/issues/90
    synced_at: '2026-04-27T11:22:47Z'
  gitee:
    issue_id: IJFO7X
    url: https://gitee.com/zhaoquan/freely/issues/IJFO7X
    synced_at: '2026-04-27T13:15:53Z'
primary_platform: github
canonical_issue_path: docs/epics/freely-product-architecture/canonical-product-posture-bootstrap-reconciliation-governance/issues/canonical-product-posture-bootstrap-reconciliation-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:22:47Z'
hash: ''
created_at: '2026-04-27T11:22:47Z'
updated_at: '2026-05-17T12:21:58Z'
platform_state: closed
---

Freely already completed the product contract and the first tool-materialization slice, but canonical `develop` still carries legacy tracked bootstrap truth:

1. `.codex/config.toml` still says `approval_policy = "on-request"` even though `auto` posture is already canonical.
2. Canonical local bootstrap state still lacks activation-consent truth, so the canonical repo reports `activation_consent_status: unknown-legacy`.
3. `freely live-status` and `freely doctor` therefore still show execution-b

canonical: docs/epics/freely-product-architecture/canonical-product-posture-bootstrap-reconciliation-governance/issues/canonical-product-posture-bootstrap-reconciliation-governance.md
