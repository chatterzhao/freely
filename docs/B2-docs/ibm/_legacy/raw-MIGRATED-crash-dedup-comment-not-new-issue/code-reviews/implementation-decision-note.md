- issue_id: I-20260522T002426Z-A
## Implementation Decision Note
- decision: Search existing OPEN issues by crash title; comment if found; create new only if not
- why_this: 950+ duplicate crash issues flooded tracker and scan, drowning real tasks
- alternatives_considered: Local dedup (can't dedup across restarts), issue labels (doesn't prevent duplicates)
- residual_risk: gh search might miss due to API pagination; mitigated by exact title match
