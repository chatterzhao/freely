---
local_id: I-20260406-1851-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '122'
    url: https://github.com/chatterzhao/freely/issues/122
    synced_at: '2026-04-27T11:25:53Z'
  gitee:
    issue_id: IJFO95
    url: https://gitee.com/zhaoquan/freely/issues/IJFO95
    synced_at: '2026-04-27T13:16:44Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/codex-interactive-login-and-apikey-input-flow-governance/issues/codex-interactive-login-and-apikey-input-flow-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:25:53Z'
hash: ''
created_at: '2026-04-27T11:25:53Z'
updated_at: '2026-05-17T12:23:26Z'
platform_state: closed
---

Freely 还缺一个受治理约束的 Codex-first interactive login contract。当前 dirty implementation 已经证明这条 UX follow-on 足够具体，但它仍悬空在未归档实现树里：

- `freely ai login codex` 还没有 canonical 的 auth-mode 交互选择
- `freely ai login codex apikey` 还没有 canonical 的 provider/base-url/api-key 输入收集与 direct-arg parity
- empty-input failure、live bundle materialization、saved-slot continuity 还没有 owner-bound acceptance

这不是重开 bundle/probe owner，也不是 current-live bootstrap 或 reconnect fast-fail。它是一个独立的 first-hop UX owner。

canonical: docs/B2-docs/config/codex-interactive-login-and-apikey-input-flow-governance/issues/codex-interactive-login-and-apikey-input-flow-governance.md
