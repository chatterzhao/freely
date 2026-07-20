- issue_id: I-20260720T051323Z-A
- issue_path: docs/B2-docs/acp/cross-tool-session/raw-20260720T051323Z/issues/I-20260720T051323Z-A.md
- phase_state: done_b2_ibm
## Implementation Decision Note
- decision: L13093 UUID regex → is_valid_session_id()
- why_this: is_valid_session_id 已支持 ses_+UUID，capture 是唯一遗漏点
- alternatives_considered: 修改 regex 同时匹配 ses_ — 驳回，重复逻辑
- boundary_non_goals: 不改 is_valid_session_id；不改其他 session 处理
- residual_risk: 无
