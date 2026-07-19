---
issue_id: I-20260719T101009Z-A
phase_state: completed
---
- decision: 同tool fork / 不同tool ensure bridge + new
- why_this: fork缓存命中 / 不同tool无法共享session
- boundary: 不改Python acp_session_connect(已正确)
