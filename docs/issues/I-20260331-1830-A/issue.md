---
local_id: I-20260331-1830-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '72'
    url: https://github.com/chatterzhao/freely/issues/72
    synced_at: '2026-04-27T11:21:28Z'
  gitee:
    issue_id: IJFO7B
    url: https://gitee.com/zhaoquan/freely/issues/IJFO7B
    synced_at: '2026-04-27T13:15:21Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/kiro-cli-runtime-availability-failure-governance/issues/kiro-cli-runtime-availability-failure-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:21:28Z'
hash: ''
created_at: '2026-04-27T11:21:28Z'
updated_at: '2026-05-17T12:21:15Z'
platform_state: closed
---

Recent dogfood runs exposed one concrete Kiro failure family:

- `Unable to verify subscription status: service error`
- `Monthly request limit reached`

Before the fix, Freely recorded these exits as plain `ai_exit_rc_0`, left `slot_switch_reason=none`, and immediately relaunched both root and worker supervisors into the same unusable path. That was not just noisy behavior; it corrupted runtime truth and hid a control-plane availability failure behind a fake healthy completion.

The minimal cor

canonical: docs/epics/workspace-routing-foundation/kiro-cli-runtime-availability-failure-governance/issues/kiro-cli-runtime-availability-failure-governance.md
