# Implementation Decision: remove 'local' from wt-close Phase 3
- issue_id: I-20260617T160807Z-A
- decision: Remove 'local' keyword from _current_phase declaration — Phase 3 is at script top level, not inside a function
- why_this: Bash rejects 'local' outside functions. Regression from a80b3072.
- alternatives_considered: Move Phase 3 into a function — rejected, overkill for one variable
- boundary_non_goals: Not restructuring wt-close architecture
- residual_risk: None
