# Code Review
- issue_id: I-20260503T1428Z-A
## Implementation Decision Note
- decision: end_turn grace period + broken pipe tolerance
- why_this: run-acp-prompt.py disconnects before bridge finishes; grep stop_reason=end_turn in cycle log → normalize rc=1→0
- alternatives_considered: (1) Grace period in run-acp-prompt.py — chosen (2) Increase RESTART_STORM_COUNT — band-aid only
- boundary_non_goals: Not restructuring bridge lifecycle, not changing session management
- residual_risk: If end_turn appears in log but AI actually failed, rc would be incorrectly normalized to 0. Defense: end_turn only written when AI completes normally.
