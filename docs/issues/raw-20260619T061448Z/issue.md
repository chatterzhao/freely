---
local_id: raw-20260619T061448Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T061448Z-A
platform_ids:
  github:
    issue_id: '3038'
    url: https://github.com/chatterzhao/freely/issues/3038
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T06:15:05Z'
updated_at: '2026-06-21T20:04:33Z'
intake_id: ''
author: platform
channel: github
session_refs: []
platform_state: closed
---

A2A server log shows 40+ 'Invalid HTTP request received' warnings since startup. Something sends non-HTTP data to the A2A unix socket. Fix: identify probe source and configure correct protocol, or add protocol detection in A2A server to suppress noise.
