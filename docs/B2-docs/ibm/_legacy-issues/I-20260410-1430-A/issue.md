---
local_id: I-20260410-1430-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '130'
    url: https://github.com/chatterzhao/freely/issues/130
    synced_at: '2026-04-27T11:26:25Z'
  gitee:
    issue_id: IJFO9F
    url: https://gitee.com/zhaoquan/freely/issues/IJFO9F
    synced_at: '2026-04-27T13:16:56Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/preferred-auth-method-account-switch-fix.md
last_synced_comment_at:
  github: '2026-04-27T11:26:25Z'
hash: ''
created_at: '2026-04-27T11:26:25Z'
updated_at: '2026-05-17T12:23:51Z'
platform_state: closed
---

When switching from an apikey slot to an account slot, the `preferred_auth_method` field is deleted from live `~/.codex/config.toml` but not restored. This happens because account slots have empty `config-auth.toml` fragments.

canonical: docs/B2-docs/config/codex-apikey-slot-bundle-and-provider-aware-probe-governance/issues/preferred-auth-method-account-switch-fix.md
