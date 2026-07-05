## Implementation Decision Note
- issue_id: I-20260624T085740Z-A
- issue_path: docs/issues/I-20260624T085740Z-A/issue.md
- decision: parse submitted + worker_count=0 + 30s grace → resume_manager; prompt "无事可做" --state completed → --state failed
- why_this: Fix #3381 空循环因果链第 2 环和第 4 环
- alternatives_considered: none — both fixes directly address root cause analysis
- boundary_non_goals: 不涉及 #3387 CSV 清理
- residual_risk: 30s grace period 可能对慢启动 worker 不够，可在后续调优
