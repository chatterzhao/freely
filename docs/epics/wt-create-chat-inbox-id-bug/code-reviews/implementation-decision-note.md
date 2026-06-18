---
issue_id: I-20260618T100000Z-A
issue_path: docs/issues/I-20260618T100000Z-A/issue.md
---

# Implementation Decision Note

## Implementation Decision Note

- issue_id: I-20260618T100000Z-A
- issue_path: docs/issues/I-20260618T100000Z-A/issue.md
- decision: Normalize chat-inbox ID by stripping TZ characters before passing to chat-inbox.py commands
- why_this: Minimal change (4 lines), follows existing pattern already used for SQL queries in same functions; chat-inbox.py explicitly expects bare IDs per its help text
- alternatives_considered: 1) chat-inbox.py handles both formats — increases complexity and testing surface; 2) Store IDs with TZ in DB — breaks existing data and requires migration
- boundary_non_goals: Does not change chat-inbox.py interface, DB schema, or affect --source platform/--source local paths
- residual_risk: Future new call sites may also forget normalization — mitigate by grep for --id.*$ts in reviews
