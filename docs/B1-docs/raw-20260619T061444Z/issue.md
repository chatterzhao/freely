---
local_id: raw-20260619T061444Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T061444Z-A
platform_ids:
  github:
    issue_id: '3037'
    url: https://github.com/chatterzhao/freely/issues/3037
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T06:15:01Z'
updated_at: '2026-06-19T06:15:01Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

ACP bridge log shows repeated JSONDecodeError + BrokenPipeError across Thread-5/6/8. Clients send empty data then disconnect, causing unhandled exceptions. Fix: add empty-line filtering before json.loads and catch BrokenPipeError gracefully in handle_client.
