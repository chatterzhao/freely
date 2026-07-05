---
local_id: I-20260429-1745-A
issue_title: Fix daemon self-detection suicide + bash 3.2 pipefail crash
kind: linked
phase_state: completed
promoted_from: raw-20260429-1745
platform_ids:
  github:
    issue_id: '216'
    url: https://github.com/chatterzhao/freely/issues/216
    synced_at: '2026-05-05T14:19:46Z'
  gitee:
    issue_id: ''
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/bash32-daemon-compat-fix/issues/I-20260429-1745-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-04-29T17:45:00Z'
updated_at: '2026-05-05T14:19:52Z'
session_refs:
- tool: ccds
  session_id: 20260429-bash32-fix
  role: author
platform_state: closed
---

## Pre-Brainstorm Summary

macOS bash 3.2 compatibility fix: two defensive changes, no core logic changes.

## Scope

Minimal changes to `docs/system/workspace/scripts/runtime/freely`.

## References

- B1: docs/B1-docs/raw-20260429/
- Issue: docs/epics/workspace-routing-foundation/bash32-daemon-compat-fix/issues/I-20260429-1745-A.md
