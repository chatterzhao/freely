# Code Review: L223 task_mode wait guard
- issue_id: I-20260510T0112Z-A
## Implementation Decision Note
- decision: L223 restart 条件加 task_mode 检查，wait 时跳过
- why_this: 一行修改，最小侵入，wait 模式下 AI 不在是预期行为
