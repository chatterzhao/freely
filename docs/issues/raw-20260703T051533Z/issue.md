---
local_id: raw-20260703T051533Z
kind: raw
phase_state: absorbed
platform_ids:
  github:
    issue_id: '3701'
    url: https://github.com/chatterzhao/freely/issues/3701
    synced_at: ''
  gitee:
    issue_id: IJYK59
    url: https://gitee.com/zhaoquan/freely/issues/IJYK59
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-07-03T05:15:54Z'
updated_at: '2026-07-03T05:15:54Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

\n\n## Bug
.gitignore has __pycache__/ but .pyc files were force-added to git. Python recompiles them on import → git sees dirty tree → daemon refuses to start.

docs/system/workspace/agents/__pycache__/input_required_reason.cpython-314.pyc
docs/system/workspace/scripts/runtime/__pycache__/acp-bridge.cpython-314.pyc
docs/system/workspace/scripts/runtime/__pycache__/agent_working.cpython-314.pyc
docs/system/workspace/scripts/runtime/__pycache__/freely_db_manager.cpython-314.pyc
docs/system/workspace/scripts/runtime/__pycache__/watchdog_sse.cpython-314.pyc
docs/system/workspace/scripts/runtime/a2a/__pycache__/a2a_types.cpython-314.pyc

## Fix
git rm --cached all .pyc files. .gitignore already covers __pycache__/.
