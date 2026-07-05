---
local_id: I-20260407-0023-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '123'
    url: https://github.com/chatterzhao/freely/issues/123
    synced_at: '2026-04-27T11:25:59Z'
  gitee:
    issue_id: IJFO97
    url: https://gitee.com/zhaoquan/freely/issues/IJFO97
    synced_at: '2026-04-27T13:16:47Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/codex-auto-switch-probe-apikey-fallback-governance/issues/codex-auto-switch-probe-apikey-fallback-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:25:59Z'
hash: ''
created_at: '2026-04-27T11:25:59Z'
updated_at: '2026-05-17T12:23:29Z'
platform_state: closed
---

Codex account/apikey bundle truth is already owned, but dogfooding exposed one remaining fallback gap after that owner closed: if the OAuth sweep returns `all_unavailable:*`, Freely still stops before exec-probing saved `apikey-*` slots. That violates the narrower contract that apikey slots use `codex exec` truth and makes no-arg `switch codex` disagree with explicit apikey switching.

canonical: docs/B2-docs/config/codex-auto-switch-probe-apikey-fallback-governance/issues/codex-auto-switch-probe-apikey-fallback-governance.md
