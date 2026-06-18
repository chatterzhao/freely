# Implementation Decision
- issue_id: I-20260618T051709Z-A
- decision: Use sed line-number insertion instead of Python string replacement for pr-merge-guarded edits
- why_this: Python replacements failed silently 3 times. Line-number insertion is deterministic.
- alternatives_considered: Refactor pr-merge-guarded to use include files — rejected, overkill
- boundary_non_goals: Not changing other pr-merge logic
- residual_risk: Line numbers may drift if file is modified. Test before merge.
