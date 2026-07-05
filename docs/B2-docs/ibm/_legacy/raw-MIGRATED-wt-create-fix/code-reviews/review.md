# Code Review: wt-create fix
- issue_id: I-20260508T120000Z-A
## Implementation Decision Note
- decision: _extract_issue_key [0-9]{4} → [0-9]{4,6}；_scan_lookup dict→items
- why_this: 阻塞所有带秒 raw-key 工位创建，必须修复
- alternatives_considered: 仅 legacy 模式（拒绝：新接口不可用）
- boundary_non_goals: 不改 wt-create 其他逻辑
- residual_risk: none
