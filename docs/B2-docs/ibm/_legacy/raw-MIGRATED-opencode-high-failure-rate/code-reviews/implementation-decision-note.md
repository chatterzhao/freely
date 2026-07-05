- issue_id: I-20260521T234624Z-A
## Implementation Decision Note
- decision: Add set+e + re-entry guard to _on_supervisor_err
- why_this: Recursive ERR trap obscured real errors and created crash spam. Original error (execution_network_transient) was lost.
- alternatives_considered: Move ERR trap after crash handler (race condition), use EXIT trap instead (different semantics)
- residual_risk: Re-entry guard may suppress legitimate follow-up errors during crash handling (acceptable trade-off)
