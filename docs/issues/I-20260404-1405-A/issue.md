---
local_id: I-20260404-1405-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '100'
    url: https://github.com/chatterzhao/freely/issues/100
    synced_at: '2026-04-27T11:23:43Z'
  gitee:
    issue_id: IJFO8E
    url: https://gitee.com/zhaoquan/freely/issues/IJFO8E
    synced_at: '2026-04-27T13:16:12Z'
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:23:43Z'
hash: ''
created_at: '2026-04-27T11:23:43Z'
updated_at: '2026-05-17T12:22:29Z'
platform_state: closed
---

Current canonical `develop` can reach manager prompt publication during `freely start`, but the control plane was not yet truthful end-to-end. The first replay exposed a bootstrap race where the watchdog restarted a fresh supervisor before `ai.pid` appeared. After that bounded grace fix, the next replay proved continuity artifacts were being written, but the manager/runtime handoff still misreported `latest_manager_worker_prompts_generated=none` because the current continuity format recorded the

canonical: docs/epics/workspace-routing-foundation/manager-bootstrap-prompt-publication-without-continuity-materialization-governance/issues/manager-bootstrap-prompt-publication-without-continuity-materialization-governance.md
