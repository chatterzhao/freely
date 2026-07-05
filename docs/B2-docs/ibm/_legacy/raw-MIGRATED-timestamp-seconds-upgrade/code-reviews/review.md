# Code Review: timestamp seconds upgrade
- issue_id: I-20260507T143545Z-A
## Implementation Decision Note
- decision: 所有 \\d{4} → \\d{4,6}，_normalize_key_variants 增加 bare→new 转换
- why_this: 6位秒的 raw-key 在正则匹配中被截断导致门禁假阳性
- alternatives_considered: 只改 _normalize_key_variants（拒绝：门禁和其他脚本的正则也会截断）
- boundary_non_goals: 不改变 key 的存储格式，只扩展正则匹配范围
- residual_risk: none
