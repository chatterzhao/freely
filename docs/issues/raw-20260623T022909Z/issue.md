---
local_id: raw-20260623T022909Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3379'
    url: https://github.com/chatterzhao/freely/issues/3379
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-23T02:29:26Z'
updated_at: '2026-06-23T02:29:26Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

task-lifecycle-scan.py line 19 uses `from platform_adapter import list_open_issues` but the file is named `platform-adapter.py` (hyphen, not underscore). Additionally, the _SYNC_DIR path on line 16 is `parent.parent / \"sync\"` but should be `parent.parent / \"scripts\" / \"sync\"`. Fix both issues so the scan can run again.
