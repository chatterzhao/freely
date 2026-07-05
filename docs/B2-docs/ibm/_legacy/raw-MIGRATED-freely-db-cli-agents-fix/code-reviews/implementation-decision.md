# Implementation Decision: freely-db-cli syntax + AGENTS.md flow + hook skill routing
- issue_id: I-20260617T145428Z-A
- decision: Three independent single-line/doc fixes — restore missing `for k in (` in freely-db-cli, restructure AGENTS.md entry as OR-branch (feedback/scan), point pre-commit hook message to skills instead of mechanical git commands
- why_this: All three bugs share root cause: missing or insufficient guidance for AI agents. Bug 1 (syntax) prevents self-diagnosis. Bug 2 (missing feedback entry) causes AI to skip intake step. Bug 3 (no skill routing in hook message) causes AI to treat governance as obstacle and seek workarounds (skip-worktree, removing remotes)
- alternatives_considered: Rewrite _task_update_params — rejected, overkill for 1-line fix. Auto-invoke skill from hook — rejected, technically infeasible from bash. Add linting — rejected, separate concern
- boundary_non_goals: Not adding automated syntax checking. Not restructuring full AGENTS.md. Not changing hook behavior beyond message text
- residual_risk: None. All changes are additive (restoring deleted syntax) or documentation-only
