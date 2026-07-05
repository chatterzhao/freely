# Code Review: platform pull title standardization
- issue_id: I-20260507T143546Z-A
## Implementation Decision Note
- decision: pull 时用平台 created_at 标准化标题 key，best-effort 不阻塞
- why_this: 用户手动创建的 issue 标题可能缺秒，需自动修正
- alternatives_considered: 仅靠 lint/检查提示（拒绝：用户体验差）
- boundary_non_goals: 不改已有 issue 的历史标题
- residual_risk: 平台 API 调用可能失败（有异常保护，不影响 pull）
