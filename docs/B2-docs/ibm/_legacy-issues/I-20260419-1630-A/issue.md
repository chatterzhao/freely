---
local_id: I-20260419-1630-A
kind: linked
phase_state: completed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: "2026-05-19T23:20:00Z"
platform_ids:
  github:
    issue_id: '157'
    url: https://github.com/chatterzhao/freely/issues/157
    synced_at: '2026-04-27T11:28:25Z'
  gitee:
    issue_id: IJFOAB
    url: https://gitee.com/zhaoquan/freely/issues/IJFOAB
    synced_at: '2026-04-27T13:17:36Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/runtime/runtime-startup-self-healing-governance/issues/runtime-startup-self-healing-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:28:25Z'
hash: ''
created_at: '2026-04-27T11:28:25Z'
updated_at: '2026-05-17T12:24:56Z'
platform_state: closed
---

Protected-root replay on `2026-04-19` showed a narrower startup seam than the existing runtime owners cover:

1. `freely daemon start` left machine-owned truth claiming `desired_runtime_state=running`, `last_supervisor_state=up`, and `last_exit_reason=starting`.
2. The corresponding `supervisor.pid` and `interruption-dispatch.pid` files remained on disk even though no owned runtime processes were alive anymore.
3. Launch-state and continuity surfaces could still point to missing worktrees or sta

canonical: docs/B2-docs/runtime/runtime-startup-self-healing-governance/issues/runtime-startup-self-healing-governance.md
