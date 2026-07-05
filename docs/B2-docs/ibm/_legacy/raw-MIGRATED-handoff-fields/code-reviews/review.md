# Code Review: handoff fields
- issue_id: I-20260511T0407Z-A
## Implementation Decision Note
- decision: handoffs 表加 4 列 + update 参数 + worker prompt 注入
- why_this: worker_blocked 后主管需要知道原因和建议
