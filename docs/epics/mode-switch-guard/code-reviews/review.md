# Code Review: mode_just_switched guard
- issue_id: I-20260510T0856Z-A
## Implementation Decision Note
- decision: task_mode_gate 加 mode_just_switched 列，write 时检测变化设 1，L223 读到 1 跳过并归零
- why_this: 一次切换一次豁免，消费完立即闭环，无需 grace period
