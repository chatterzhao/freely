---
local_id: raw-20260703T234313Z13Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260703T234313Z-A
platform_ids:
  github:
    issue_id: '3719'
    url: https://github.com/chatterzhao/freely/issues/3719
    synced_at: ''
  gitee:
    issue_id: IJYPVF
    url: https://gitee.com/zhaoquan/freely/issues/IJYPVF
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-03T23:43:33Z'
updated_at: '2026-07-03T23:43:33Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## Bug
governance-merge-gate:1633-1636 treats 'phase_state=completed + capability changes'
as a WARNING for 'legacy issues with post-completion fixes'. This allows
incomplete IBM artifacts to bypass gate.

## Fix
1. Change WARNING to ERROR (block the merge)
2. Update error message to explain: set phase_state correctly (done_b2_ibm → in_dev/staged → completed), don't shortcut
3. Update workflow skill: emphasize NO shortcut for small changes, full workflow required
4. Update workflow skill: add --no-verify guidance (only for emergency)
