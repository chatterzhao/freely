- issue_id: I-20260703T170237Z-A
## IDN
- decision: rc!=0 时 cp cycle_debug_log 到持久 crash log
- why_this: debug log 含 stderr，当前重启即清理
- alternatives_considered: 单独捕获 stderr → 需改 launch 流程，侵入大
- boundary_non_goals: 不改变 launch 流程
- residual_risk: crash log 无自动清理，需手动管理
