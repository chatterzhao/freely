# Implementation Decision
- issue_id: I-20260618T050413Z-A
- decision: Scope git ls-files --others to governance directories (docs/issues/, pre-brainstorms/, epics/, system/) instead of repo root
- why_this: Prevents false blocks from .DS_Store, editor swap files, build artifacts while still catching commit omissions in governance docs
- alternatives_considered: Add all common temp files to .gitignore — rejected, infinite maintenance burden. Use git clean -n with .gitignore — rejected, doesn't show staged changes.
- boundary_non_goals: Not adding .gitignore management
- residual_risk: Untracked source files (new .sh scripts outside docs/) would be missed, but those should be git-added immediately after creation
