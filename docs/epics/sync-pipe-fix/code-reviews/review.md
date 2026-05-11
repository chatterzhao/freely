# Code Review: sync pipe fix
- issue_id: I-20260511T0019Z-A
## Implementation Decision Note
- decision: 替代双 python3 管道为单进程 SQLite 直查
- why_this: 管道中任一进程失败都静默吞错，单进程直接可控
