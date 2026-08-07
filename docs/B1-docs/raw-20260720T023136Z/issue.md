---
local_id: raw-20260720T023136Z
kind: raw
phase_state: absorbed
absorbed_into: I-20260720T023136Z-A
platform_ids:
  github:
    issue_id: '4038'
    url: https://github.com/chatterzhao/freely/issues/4038
    synced_at: ''
  gitee:
    issue_id: IK27DW
    url: https://gitee.com/zhaoquan/freely/issues/IK27DW
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-20T02:32:01Z'
updated_at: '2026-07-20T02:32:01Z'
intake_id: ''
author: platform
channel: github
session_refs: []
promoted_children:
- I-20260720T023136Z-A
platform_state: closed
---

# fix: chat error message shell quoting bug at l6666

## Problem
freely script L6666 contains `<描述>` and `<详细描述>` characters in a shell string that bash interprets as file redirection operators, causing:
```
line 6666: 描述: No such file or directory
```

## Root Cause
```bash
log_error "[chat]   freely feedback --title \"fix|feat: <描述>\" --kind fix --body \"<详细描述>\""
```
The `<>` characters are interpreted by bash as redirect operators, not literal characters.

## Fix
Escape or quote the angle brackets properly so they are printed as literal text.

## Evidence
Reproduced every Manager cycle when worker chat tries local raw issue creation (which is blocked). The error message itself crashes before it can be displayed to the user.

### comment-20260807T121137Z
- source: system
- event: promote_finalized
- children: ["I-20260720T023136Z-A"]

拆解为以下任务:
1. [I-20260720T023136Z-A](will-be-updated)
