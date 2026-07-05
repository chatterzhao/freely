---
candidate_id: C-20260626T121349Z-A
status: absorbed
source_raw: raw-20260626T121349Z49Z
milestone: M-20260626T121349Z-A
---

## C-20260626T121349Z-A: legacy issue

- candidate_format_version: v2
- title: Post-refactoring documentation and tool consistency cleanup
- status: absorbed
- absorbed_into: I-20260626T121349Z-A
- decision_reason: Multi-agent architecture changes left stale docs and field names
- acceptance_criteria:
  - agent-table-query help matches actual agent-table.toml format
  - test-pre-merge constraints correctly documented
  - cherry-pick replaces stash in fix-execution
- promotion_gate: Code changes + docs updated
- promoted_issue_path: docs/issues/I-20260626T121349Z-A/issue.md
- milestone: M-20260626T121349Z-A
