---
local_id: raw-20260601T030623Z
kind: raw
phase_state: absorbed
absorbed_into: raw-20260601T030623Z
absorbed_at: "2026-06-01T03:06:39Z"
dropped_reason: Fix applied via fix/raw-20260601T030623Z-cross-platform-fixes commit
  b33dff5a. Cross-platform compatibility for timeout (Linux) and stat (Linux -c %Y
  fallback). No B1/B2 needed — direct fix-execution path.
platform_state: closed
platform_ids:
  github:
    issue_id: '2391'
    url: https://github.com/chatterzhao/freely/issues/2391
    synced_at: ''
primary_platform: github
canonical_issue_path: ''
last_synced_comment_at: {}
hash: ''
created_at: '2026-06-01T03:06:39Z'
updated_at: '2026-06-13T12:33:16Z'
intake_id: ''
author: platform
channel: github
session_refs: []
---

Develop has 3 dirty files with runtime improvements:\n- freely: Linux timeout + stat -c %Y fallback\n- monitor-ai-acp.sh: Linux stat -c %Y fallback\n- .githooks/reference-transaction.debug: debug hook (untracked)\n\nThese need a feature worktree for proper commit.
