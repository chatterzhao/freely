---
local_id: raw-20260703T114618Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3707'
    url: https://github.com/chatterzhao/freely/issues/3707
    synced_at: ''
  gitee:
    issue_id: IJYP2U
    url: https://gitee.com/zhaoquan/freely/issues/IJYP2U
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-03T11:46:40Z'
updated_at: '2026-07-03T11:46:40Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## Bug
agent_working records only written for worker/reviewer (watchdog_sse.py).
Manager session creation (start-lead-agent.sh → ACP) never writes __manager__.

## Design
agent_working should be the universal session registry — write on every ACP session create, all roles. Enables unified recovery: read agent_working → get session_id → resume.
