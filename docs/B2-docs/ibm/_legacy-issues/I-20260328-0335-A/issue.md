---
local_id: I-20260328-0335-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '65'
    url: https://github.com/chatterzhao/freely/issues/65
    synced_at: '2026-04-27T11:21:04Z'
  gitee:
    issue_id: IJFO73
    url: https://gitee.com/zhaoquan/freely/issues/IJFO73
    synced_at: '2026-04-27T13:15:12Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/manager-supervision-quiet-period-stall-signal-governance/issues/manager-supervision-quiet-period-stall-signal-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:21:04Z'
hash: ''
created_at: '2026-04-27T11:21:04Z'
updated_at: '2026-05-17T12:20:53Z'
platform_state: closed
---

`I-20260323-1705-A` 已经把 manager delegated continuation stall recovery 收紧到 `same-lane busy` 的 lawful wait 边界，但真实 dogfood 继续暴露出更深一层的问题：

- manager 与 active worker 都存活
- delegated continuation 已进入当前 manager prompt
- `pending_delegated_continuation_ids` 已清空
- 但 manager 只要在监督轮次里静默约 `90s`，runtime 仍会触发
  - `runtime-stalled-ai-recovery`
  - `local_continuation_reentry`
  - `operator_stop_requested`

这说明当前 stall detector 仍把 delegated-supervision quiet-period 近似成强 stall 证据。三个 loop 的设计并不要求 manager 在监督 acti

canonical: docs/epics/workspace-routing-foundation/manager-supervision-quiet-period-stall-signal-governance/issues/manager-supervision-quiet-period-stall-signal-governance.md
