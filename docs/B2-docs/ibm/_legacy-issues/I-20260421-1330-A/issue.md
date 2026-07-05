---
local_id: I-20260421-1330-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '161'
    url: https://github.com/chatterzhao/freely/issues/161
    synced_at: '2026-04-27T11:28:45Z'
  gitee:
    issue_id: IJFOAI
    url: https://gitee.com/zhaoquan/freely/issues/IJFOAI
    synced_at: '2026-04-27T13:17:42Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/ibm/absorbed-merged-lane-routing-followthrough-governance/issues/absorbed-merged-lane-routing-followthrough-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:28:45Z'
hash: ''
created_at: '2026-04-27T11:28:45Z'
updated_at: '2026-05-17T12:25:08Z'
platform_state: closed
---

The previous runtime repairs already blocked automatic relaunch of merged worker lanes. The remaining failure was subtler: manager patrol still looked at absorbed merged lanes and treated them like current execution capacity.

Two bounded surfaces caused that drift:

1. `wt-fleet-status` preserved `LAST_ROLE_HINT=worker` even when the branch tip was already absorbed into `develop`.
2. `task-source-scan` kept routing linked progress items back to `verification` because it did not consult the link

canonical: docs/B2-docs/ibm/absorbed-merged-lane-routing-followthrough-governance/issues/absorbed-merged-lane-routing-followthrough-governance.md
