# Implementation Decision: wt-close remote branch deletion fix
- issue_id: I-20260618T031437Z-A
- decision: Fix SELF_ROOT→PROJECT_ROOT for gitee API path; replace silent failure (2>/dev/null || true) with warning message for git push --delete
- why_this: 9 stale remote branches found on GitHub after local wt-close. SELF_ROOT undefined in standalone script. Silent failures hide real problems.
- alternatives_considered: Run separate cleanup script periodically — rejected, wt-close should handle this atomically
- boundary_non_goals: Not adding retry logic for failed deletions
- residual_risk: git fetch may still fail for already-deleted branches, but we now attempt push --delete regardless
