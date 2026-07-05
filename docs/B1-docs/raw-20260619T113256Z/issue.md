---
local_id: raw-20260619T113256Z56Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260619T113256Z-A
platform_ids:
  github:
    issue_id: '3059'
    url: https://github.com/chatterzhao/freely/issues/3059
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-19T11:33:13Z'
updated_at: '2026-06-19T11:33:13Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

## Two bugs blocking worker delegation

### Bug 1: a2a_task.py list() transports
list() uses _request()→_unix_request()→JSON-RPC tasks/list. Returns empty.
create() and update() use _rest_request()→REST HTTP. Works correctly.
Fix: change list() line 251 from _request to _rest_request.

### Bug 2: Runtime consumer doesnt unpack rows dict
freely script line 12827: json.load() returns {'rows': [...]}. Iterating
dict gives key 'rows' string, not tasks. .get() on string fails → silent skip.
Fix: for r in rows.get('rows', []): instead of for r in rows:

Verified: after fixes, Manager's a2a-exit worker tasks correctly appear in
list --role worker --status submitted with all 28 fields.
