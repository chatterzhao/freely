- issue_id: I-20260521T132714Z-A
- issue_path: docs/issues/I-20260521T132714Z-A/issue.md
## Implementation Decision Note
- decision: Add bridge pid cleanup in stop_project_runtime before the restart case block
- why_this: Bridge was only killed in the default switch case after supervisor cleanup, and pkill -f was too broad. Using tracked pid is precise.
- alternatives_considered: Fix _stop_acp_bridge pkill scope (broader fix), add pid to supervisor child tracking (more complex)
- boundary_non_goals: Not removing _stop_acp_bridge (still needed for supervisor self-cleanup). Not changing bridge startup pid tracking.
- residual_risk: If bridge pid file is stale/wrong, cleanup is skipped gracefully
