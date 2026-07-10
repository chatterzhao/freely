---
kind: raw
priority: P2
phase_state: absorbed
source: feedback
created_at: '2026-05-18T02:57:49Z'
title: 'runtime crisis: all worker launches fail (stale_pid / launch_failed)'
platform_ids:
  github:
    issue_id: '547'
    url: https://github.com/chatterzhao/freely/issues/547
    synced_at: '2026-05-18T02:57:56Z'
updated_at: '2026-06-17T00:19:51Z'
primary_platform: github
platform_state: closed
local_id: raw-20260518T025749Z---

Systemic bug: every single worker launched since 2026-05-16 has failed with stale_pid or launch_failed (50 rejected + countless stale_pid). Root cause: supervisor repeatedly crashes with 'bash at freely:18777 (rc=0)' - already logged as issues #544, #545, #546.

Impact: zero workers have completed in the last 48+ hours. All management actions requiring delegation (merge, retire, closeout) are blocked until this is fixed.

Next: investigate the worker launch mechanism in the runtime scripts and fix the supervisor crash loop.
