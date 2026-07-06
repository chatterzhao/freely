---
local_id: I-20260328-0745-A
kind: linked
phase_state: absorbed
- verification_artifact_dir: docs/B2-docs/ibm/_legacy-issues/raw-20260328-0745/code-reviews
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '66'
    url: https://github.com/chatterzhao/freely/issues/66
    synced_at: '2026-04-27T11:21:08Z'
  gitee:
    issue_id: IJFO74
    url: https://gitee.com/zhaoquan/freely/issues/IJFO74
    synced_at: '2026-04-27T13:15:13Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/live-status-current-runtime-state-reconciliation-governance/issues/live-status-current-runtime-state-reconciliation-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:21:08Z'
hash: ''
created_at: '2026-04-27T11:21:08Z'
updated_at: '2026-05-17T12:20:56Z'
platform_state: closed
---

`live-status` is the current-state entrypoint, but it could surface an internally contradictory answer:

- `activity_state: ai_active`
- `last_ai_state: down`
- `last_exit_reason: starting`

The contradiction came from reading current runtime PID truth and persisted `workcell-state.env` independently without any reconciliation step.

canonical: docs/B2-docs/ibm/live-status-current-runtime-state-reconciliation-governance/issues/live-status-current-runtime-state-reconciliation-governance.md
