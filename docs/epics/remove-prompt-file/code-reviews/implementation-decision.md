# Implementation Decision: Remove prompt_file from A2A
- issue_id: I-20260617T110109Z-A
- reviewer: claude-sonnet-4-6
- review_date: 2026-06-17
- decision: Remove prompt_file from all A2A files, derive path from task_id at Runtime
- why_this: A2A protocol uses Message for content, not file paths
- alternatives_considered: Keep prompt_file — rejected: ACP detail leaking into A2A
- boundary_non_goals: DB column stays for backward compat (stops writing)
- residual_risk: Old worker tasks with prompt_file field may not have message populated
