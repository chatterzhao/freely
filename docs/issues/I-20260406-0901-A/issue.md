---
local_id: I-20260406-0901-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '119'
    url: https://github.com/chatterzhao/freely/issues/119
    synced_at: '2026-04-27T11:25:38Z'
  gitee:
    issue_id: IJFO91
    url: https://gitee.com/zhaoquan/freely/issues/IJFO91
    synced_at: '2026-04-27T13:16:40Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/issues/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:25:38Z'
hash: ''
created_at: '2026-04-27T11:25:38Z'
updated_at: '2026-05-17T12:23:17Z'
platform_state: closed
---

Freely 已经把 Codex API-key slot bundle、provider-aware probe routing、以及 runtime network-failure taxonomy 分别冻结为 canonical contract，但 dogfood 现场仍暴露一个新边界：

- `codex exec "hi"` 已经输出明确的 `ERROR: Reconnecting...` / connection-failure 证据
- probe 仍然继续占着 slot-switch lock 等待完整 timeout
- `ai status` / `ai switch codex` / manager bootstrap 因此把 incident 表现成 generic timeout，而不是 network-local failure

这不是重开旧的 slot bundle owner，也不是重写 runtime recovery state machine。需要一个新的 follow-on owner，专门冻结 “partial-output reconne

canonical: docs/epics/workspace-routing-foundation/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance/issues/codex-reconnect-probe-fast-fail-and-runtime-network-classification-governance.md
