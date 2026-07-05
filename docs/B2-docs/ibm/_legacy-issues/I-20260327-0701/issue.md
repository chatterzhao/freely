---
local_id: I-20260327-0701
kind: linked
phase_state: dropped
completed_at: '2026-06-16T04:14:56Z'
platform_ids:
  github:
    issue_id: '61'
    url: https://github.com/chatterzhao/freely/issues/61
    synced_at: '2026-04-27T11:17:58Z'
  gitee:
    issue_id: IJFO6X
    url: https://gitee.com/zhaoquan/freely/issues/IJFO6X
    synced_at: '2026-04-27T13:15:06Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/pre-tests-evidence-binding-and-completion-gate-governance/issues/pre-tests-evidence-binding-and-completion-gate-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:17:58Z'
hash: ''
created_at: '2026-04-27T11:17:58Z'
updated_at: '2026-04-27T11:17:58Z'
platform_state: closed
---

The observed miss was not that Freely lacked tests in the abstract. High-level truth already required `Unit / Integration / End-to-End / Real-Environment`, and the gates already checked that those sections existed. The gap was narrower and more serious:

1. recent auth/switch follow-on owners could dual-waive `End-to-End` and `Real-Environment`
2. the gate only checked the current owner contract, so those waivers looked structurally valid
3. real `bin/ai`, real `codex exec`, and real `freely sta

canonical: docs/epics/workspace-routing-foundation/auth-switch-real-environment-and-e2e-adequacy-governance/issues/auth-switch-real-environment-and-e2e-adequacy-governance.md
