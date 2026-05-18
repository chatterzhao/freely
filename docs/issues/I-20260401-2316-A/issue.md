---
local_id: I-20260401-2316-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '86'
    url: https://github.com/chatterzhao/freely/issues/86
    synced_at: '2026-04-27T11:22:24Z'
  gitee:
    issue_id: IJFO7S
    url: https://gitee.com/zhaoquan/freely/issues/IJFO7S
    synced_at: '2026-04-27T13:15:46Z'
primary_platform: github
canonical_issue_path: docs/epics/freely-product-architecture/cc-acp-init-autonomy-consent-test-followthrough-governance/issues/cc-acp-init-autonomy-consent-test-followthrough-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:22:24Z'
hash: ''
created_at: '2026-04-27T11:22:24Z'
updated_at: '2026-05-17T12:21:46Z'
platform_state: closed
---

`I-20260401-1303-A-2` already froze the activation-consent and tool materialization contract for `cc:auto`. The remaining failure on canonical `develop` is not a new product question; it is a stale test invocation on the `cc:auto + --tool-adapter acp` init path.

Because the develop merge gate requires every develop-bound replay to remain candidate-driven, this followthrough needs its own narrow owner instead of silently editing a completed-family surface.

canonical: docs/epics/freely-product-architecture/cc-acp-init-autonomy-consent-test-followthrough-governance/issues/cc-acp-init-autonomy-consent-test-followthrough-governance.md
