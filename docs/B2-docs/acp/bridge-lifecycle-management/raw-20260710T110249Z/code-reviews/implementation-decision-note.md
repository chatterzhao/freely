---
issue_id: I-20260710T110249Z-A
phase_state: done_b2_ibm
---
- issue_id: I-20260710T110249Z-A
## IDN
- decision: monitor 直接传 base_tool; freely 用 manager base_tool 作为默认值
- why_this: 11处默认路径调用导致 bridge 检测/启停/清理全部盲区
- boundary_non_goals: 不改变 ACP session 函数的 role→base_tool 查找
- residual_risk: 非 manager bridge 的启停仍使用 manager 路径（低风险）
