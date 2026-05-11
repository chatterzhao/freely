# Code Review: worker handoff inject
- issue_id: I-20260511T0229Z-A
## Implementation Decision Note
- decision: worker launch 前注入 handoff_id + db_path 到 prompt，worker 直接写中心 DB
- why_this: 消除工位隔离导致的 handoff 不可达，worker 不再需要自己的 DB
