- issue_id: I-20260521T121158Z-A
- issue_path: docs/issues/I-20260521T121158Z-A/issue.md
## Implementation Decision Note
- decision: Add THHMMZ to nightly version format
- why_this: Same-day rebuilds need distinguishable versions
- alternatives_considered: Using unix timestamp (too opaque), keeping old format (ambiguous)
- boundary_non_goals: Not changing stable version format
- residual_risk: None
