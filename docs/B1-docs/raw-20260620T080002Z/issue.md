---
local_id: raw-20260620T080002Z02Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260620T080002Z-A
platform_ids:
  github:
    issue_id: '3151'
    url: https://github.com/chatterzhao/freely/issues/3151
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-20T08:00:19Z'
updated_at: '2026-06-20T08:00:19Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

PR #3147 changed manager_max_parallel_workers() from 'unbounded' to '10:7', but two callers (lines 8746 and 10849) still check for 'unbounded'. When they receive '10:7', the comparison fails, bash enters arithmetic code paths with string '10:7', crashes with set -e, and kills the entire daemon start process silently.

Additionally, manager_worker_launch_available_slots() at line 12210 still returns hardcoded 'unbounded' — should compute from manager_max_parallel_workers.

Fix: apply same max:warn parsing to all three locations.
