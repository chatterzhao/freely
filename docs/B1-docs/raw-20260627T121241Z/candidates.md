---
candidate_id: C-20260627T121241Z-A
status: promoted
source_raw: raw-20260627T121241Z
created_at: 2026-06-27
milestone: M-20260627T121241Z-A
---

## C-20260627T121241Z-A: legacy issue

- candidate_format_version: v2
- title: scan agent-id.env path + sessions query fix
- status: promoted
- decision_reason: agent-id.env at develop/.freely, not worktree-local
- next_action: B2_IBM -> dev -> pr-merge
- acceptance_criteria:
  - agent-id.env path set to project-global
  - parse format matches {path}={role}={id}
  - sessions query compatible with both generic and specific role
- promotion_gate: scan Cat 3 correctly reads agent-id.env
- promoted_issue_path: docs/issues/I-20260627T121241Z-A/issue.md
- milestone: M-20260627T121241Z-A
