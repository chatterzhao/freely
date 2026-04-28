# Fix rc=1 SessionEnd normalization - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Check debug log for SessionEnd:...completed with status 0 after ai process exit. If found, normalize rc=1 to rc=0 before recording exit reason.`
- why_this: `Claude Code -p mode exits rc=1 after SessionEnd:other even when the session completed cleanly. This caused the daemon to loop: fresh → rc=1 → resume fail → fresh → repeat.`
- alternatives_considered: `1) Fix claude exit code: can't (upstream behavior). 2) Skip all rc=1: too broad, real errors exist. 3) Check SessionEnd in debug log: chosen, precise signal.`
- boundary_non_goals: `No change to actual error handling. Only normalizes rc when SessionEnd confirms clean completion.`
- residual_risk: `If SessionEnd matches but there was a genuine error earlier, we might miss it. Mitigated: the AI cycle produces debug evidence; if no work is done, next scan will surface stale state.`

## Verification
- bash -n: `pass`
- debug log with SessionEnd completed status 0: `pass` (rc normalized to 0)
- debug log without SessionEnd: `pass` (rc unchanged)
- missing debug log: `pass` (condition short-circuits gracefully)
