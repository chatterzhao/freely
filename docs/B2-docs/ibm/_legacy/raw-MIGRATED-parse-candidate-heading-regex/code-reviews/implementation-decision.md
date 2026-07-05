---
issue_id: I-20260619T035704Z-A
issue_path: docs/issues/I-20260619T035704Z-A/issue.md
phase_state: done_b2_ibm
---

- issue_id: I-20260619T035704Z-A
- issue_path: docs/issues/I-20260619T035704Z-A/issue.md

## Implementation Decision Note

- decision: Change regex from `^##{1,3}` to `^#{1,3}` in parse_candidate_file heading detection. Also add diagnostic hint when candidate file exists but has no matching heading.
- why_this: Single `#` is valid markdown; gate should accept it. The existing regex silently returns 0 records, causing confusing "no valid source_candidate" errors with no diagnostic.
- alternatives_considered: (A) Document the ## requirement in skills — doesn't prevent the user error. (B) Accept #{1,3} — simple, backward-compatible, fixes root cause.
- boundary_non_goals: Not changing candidate status logic, milestone validation, or promotion gate. Purely a heading recognition fix.
- residual_risk: None. #{1,3} is a strict superset of ##{1,3}; existing ## headings still match.
