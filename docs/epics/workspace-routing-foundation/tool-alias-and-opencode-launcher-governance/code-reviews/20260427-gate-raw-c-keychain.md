# Gate raw→C key chain enforcement - verification
- issue_id: `I-20260426-0000-A`
## Implementation Decision Note
- decision: `Enforce raw→C key chain validation in governance-merge-gate. Promoted candidates without matching raw-* issue are now hard errors.`
- why_this: `B1 input sources are now all platform issues. Every promoted candidate must trace back to a raw issue with shared date-time key.`
- alternatives_considered: `1) Keep pass/no-op: rejected, defeats purpose of B1 input tracing. 2) Warning only: rejected, too soft. 3) Hard error: chosen, ensures every promoted candidate has a raw source.`
- boundary_non_goals: `No scan update to create raw-* entries from platform issues (CHG 3.4).`
- residual_risk: `Historical promoted candidates without raw-* entries will fail the gate until scan creates raw-* entries for them.`
