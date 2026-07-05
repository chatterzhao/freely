# Candidates

## C-20260318T121000Z-A: legacy issue

- problem: Codex supervisor 在 rate-limit backoff 后可能因为长 sleep 而错过较早恢复的账号，导致恢复时间已过仍 `ai down`。
- change:
  - runtime 增加 `codex_any_saved_account_available_now`
  - 长 backoff 改为分段 sleep，周期性重判 stop marker 与账号可用性
  - 补 `test-freely-ai-account-switch`
- acceptance_hint:
  - 若某账号的 5 小时窗口先于其他账号恢复，supervisor 不得继续睡到更长窗口
  - 状态里不再长时间停留在“已过 reset_at 但 ai down”
- promoted_issue_path: pending://issue-materialization
- milestone: pending://milestone-binding
- session_refs: []
