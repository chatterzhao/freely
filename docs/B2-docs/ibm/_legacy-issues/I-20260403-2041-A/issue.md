---
local_id: I-20260403-2041-A
kind: linked
phase_state: absorbed
absorbed_at: '2026-05-16T14:27:11Z'
completed_at: '2026-04-29'
platform_ids:
  github:
    issue_id: '95'
    url: https://github.com/chatterzhao/freely/issues/95
    synced_at: '2026-04-27T11:23:15Z'
  gitee:
    issue_id: IJFO85
    url: https://gitee.com/zhaoquan/freely/issues/IJFO85
    synced_at: '2026-04-27T13:16:04Z'
primary_platform: github
canonical_issue_path: docs/B2-docs/config/packaging/issues/worktree-tool-boundary-bootstrap-governance.md
last_synced_comment_at:
  github: '2026-04-27T11:23:15Z'
hash: ''
created_at: '2026-04-27T11:23:15Z'
updated_at: '2026-05-17T12:22:13Z'
platform_state: closed
---

Freely already knows that owner development must stay in sibling feature worktrees, and it already distinguishes project-scoped command semantics from shared/global restart state. What it still lacks is a lawful runtime path for the case where the current operator sandbox cannot write the default `$FREELY_HOME` and cannot run `/bin/ps`.

Without this owner, a sandboxed session can lose both sanctioned recovery paths:

1. direct Git ownership work in the intended worktree is blocked by sandbox me

canonical: docs/B2-docs/ibm/sandbox-compatible-runtime-bootstrap-and-operator-state-governance/issues/sandbox-compatible-runtime-bootstrap-and-operator-state-governance.md
