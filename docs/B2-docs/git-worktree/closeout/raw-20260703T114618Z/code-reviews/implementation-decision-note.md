- issue_id: I-20260703T114618Z-A
## Implementation Decision Note
- decision: 在 _persist_session_anchor_early() 中按 role 写入 agent_working，manager 用 __manager__ key，UPSERT
- why_this: 该函数是每个 AI cycle 的锚点，session_id 已知，已在此写 session-state.env + session-store
- alternatives_considered: daemon startup 写 → 否决（无 session_id）；watchdog_sse 单独写 → 否决（不统一）
- boundary_non_goals: 不修改 watchdog_sse.py 的 worker/reviewer 写入（已正确）
- residual_risk: session_id 为空时记录不完整，但 manager_id 足够让 _handle_needs_manager 创建新 session
