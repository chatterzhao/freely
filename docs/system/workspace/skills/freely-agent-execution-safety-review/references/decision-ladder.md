# Decision Ladder

1. `security_review_mode: none`
- 含义：execution boundary 已对齐，无需额外 reviewer
- 动作：当前 agent 继续推进

2. `security_review_mode: single-reviewer`
- 含义：存在 posture warning，但还没到必须停机或委员会复核
- 动作：拉起 1 个 security-focused reviewer，输出 reviewer-backed continuation guidance

3. `security_review_mode: decision-committee`
- 含义：execution boundary 已失败，单 agent 不应独断继续
- 动作：拉起 2 个或更多独立 reviewer，形成内部 decision committee
- 默认 guidance：先修复 boundary，再 recheck；`minimal_risk_state` 仅作为 last-resort fallback
