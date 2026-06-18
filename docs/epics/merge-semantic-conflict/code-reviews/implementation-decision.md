# Implementation Decision: merge semantic conflict detection
- issue_id: I-20260618T035220Z-A
- decision: Add post-merge receipt check in pr-merge-guarded + actionable error in reference-transaction hook
- why_this: ef251886/15fa666c showed that git auto-merge silently drops functionality. Defensive checks prevent regression.
- alternatives_considered: Pre-merge semantic diff analysis — rejected, too complex for now
- boundary_non_goals: Not adding full semantic diff. Not changing git merge behavior.
- residual_risk: Only checks receipt, not arbitrary semantic changes
