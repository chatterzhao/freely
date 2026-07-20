- issue_id: I-20260720T045011Z-A
- issue_path: docs/B2-docs/acp/cross-tool-session/raw-20260720T045011Z/issues/I-20260720T045011Z-A.md
- phase_state: done_b2_ibm

## Implementation Decision Note
- decision: L13093 硬编码 UUID regex 替换为 is_valid_session_id()
- why_this: is_valid_session_id L4028 已支持 ses_+UUID 双格式，被多处验证使用。capture 函数是唯一遗漏点
- alternatives_considered: 修改 regex 同时匹配 ses_ — 驳回，重复逻辑，应复用已有函数
- boundary_non_goals: 不改 is_valid_session_id 本身；不改其他 session ID 处理逻辑
- residual_risk: 无。is_valid_session_id 已被其他调用点验证
