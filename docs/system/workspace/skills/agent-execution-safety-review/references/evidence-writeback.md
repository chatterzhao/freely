# Evidence Writeback

写回 reviewer-backed continuation guidance 时，至少保留：

- `execution_boundary_audit_status`
- `execution_boundary_audit_detail`
- `security_review_mode`
- `recommended_reviewer_count`
- `recommended_review_scope`
- `security_review_decision`
- `continuation_guidance`
- `minimal_risk_state`

这些字段应进入 issue / progress / verification / runtime handoff 中至少一个可追踪面，避免后续仅靠会话记忆解释为什么继续、为什么停、为什么要 reviewer。
