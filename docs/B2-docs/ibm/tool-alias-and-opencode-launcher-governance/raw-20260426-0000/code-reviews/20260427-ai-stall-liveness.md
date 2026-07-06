# AI stall detection with liveness signals - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Add _ai_shows_liveness() with debug log mtime + process state checks. All three stall functions use it before declaring AI stalled.`
- why_this: `90s cycle-log mtime timeout falsely killed AI during first-hop bootstrap (60KB+ prompt reading). Multi-signal check prevents false stalls.`
- alternatives_considered: `1) Just increase timeout: rejected, doesn't fix root cause. 2) Check only debug log: chosen as primary signal, plus process state as fallback.`
- boundary_non_goals: `No change to stall function callers. No config additions.`
- residual_risk: `Debug log may not exist for some tools. Process state check is fallback.`
