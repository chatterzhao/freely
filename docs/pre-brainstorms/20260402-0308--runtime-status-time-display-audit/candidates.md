# Runtime Status Time Display Audit Candidates

- candidate: `runtime-status-time-display-audit`
  - problem: `freely` runtime 的多个 status surfaces 仍直接展示 ISO/UTC 真相时间，和已经本地化的 frontend probe / ai-cli / watchdog 输出不一致。
  - promoted_issue_path: pending://issue-materialization
  - milestone: pending://milestone-binding
  - session_refs: []
  - desired_outcome:
    - `activation_consent_recorded_at`
    - `last_state_updated_at`
    - `develop_push_followthrough_defer_updated_at`
    - intake snapshot 中面向人的 `created_at`
    统一按宿主系统时区渲染，并显式带时区标签。
  - non_goals:
    - 不改持久化字段
    - 不改 `.bak` 备份命名
    - 不改 epoch / RFC3339 truth
  - verification:
    - `freely live-status` 的固定时间 fixture 在 `TZ=America/Los_Angeles` 下显示为本地时间
    - `freely develop-push defer` 相关输出包含本地时区标签
