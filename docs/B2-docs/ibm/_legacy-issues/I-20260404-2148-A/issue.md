---
local_id: I-20260404-2148-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '102'
    url: https://github.com/chatterzhao/freely/issues/102
    synced_at: '2026-04-27T11:23:52Z'
  gitee:
    issue_id: IJFO8G
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8G
    synced_at: '2026-04-27T13:16:15Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/slot-switch-startup-preflight-and-lock-observability-governance/issues/slot-switch-startup-preflight-and-lock-observability-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:23:52Z'
hash: ''
created_at: '2026-04-27T11:23:52Z'
updated_at: '2026-06-21T15:21:50Z'
platform_state: closed
---

Canonical `develop` has already shown two distinct truths on 2026-04-04:

1. a stale shared `~/.codex/slot-switch.lock` could block `freely start` until an operator manually removed it
2. the latest repeated root startup failures are no longer caused by a current lock and now exit with `auth_failure`

That combination means the immediate operator diagnosis is currently too implicit. Lower-layer launchers already contain partial stale-cleanup and bounded-wait behavior, but Freely still lacks a go

canonical: docs/B2-docs/config/slot-switch-startup-preflight-and-lock-observability-governance/issues/slot-switch-startup-preflight-and-lock-observability-governance.md
