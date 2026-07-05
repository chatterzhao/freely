---
local_id: I-20260502-1028-A
issue_title: 'fix: clean stale start lock before daemon stop'
kind: linked
phase_state: completed
promoted_from: raw-20260502-1028
platform_ids:
  github:
    issue_id: '210'
    url: https://github.com/chatterzhao/freely/issues/210
    synced_at: '2026-05-05T11:51:40Z'
  gitee:
    issue_id: ''
primary_platform: github
canonical_issue_path: docs/epics/workspace-routing-foundation/stale-start-lock-cleanup/issues/I-20260502-1028-A.md
last_synced_comment_at: {}
hash: ''
created_at: '2026-05-02T10:28:00Z'
updated_at: '2026-05-05T11:51:46Z'
session_refs:
- tool: ccds
  session_id: 20260502-stale-lock
  role: author
platform_state: 
---

## Summary

3-line fix in stop_project_runtime(): clean stale start lock before acquiring lock for daemon stop.

## Scope

One function call added before lock acquisition. No other changes.

## References

- B1: docs/B1-docs/raw-20260502/
- Issue: docs/epics/workspace-routing-foundation/stale-start-lock-cleanup/issues/I-20260502-1028-A.md
- Progress: docs/progress/workspace-routing-foundation/p-stale-start-lock-cleanup.md
