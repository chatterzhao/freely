---
local_id: raw-20260703T170237Z37Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260703T170237Z-A
platform_ids:
  github:
    issue_id: '3716'
    url: https://github.com/chatterzhao/freely/issues/3716
    synced_at: ''
  gitee:
    issue_id: IJYPPY
    url: https://gitee.com/zhaoquan/freely/issues/IJYPPY
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-03T17:02:59Z'
updated_at: '2026-07-03T17:02:59Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## Bug
When AI process (opencode/claude/codex) exits with rc!=0, the cycle debug log
containing stderr is cleaned up on restart. Crash root cause is lost.

## Fix
At rc!=0 detection point, copy cycle_debug_log to persistent crash log:
  .freely/logs/crash-{tool}-{timestamp}.log

Uses $AI_TOOL (registry-derived), not hardcoded — works for any tool.
