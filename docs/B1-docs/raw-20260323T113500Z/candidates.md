# 候选：codex-account-active-probe-governance

- id: `C-20260323T113500Z-A`
- title: Codex account active probe and cooldown recovery governance
- source_brainstorm: `docs/B1-docs/raw-20260323-1135/brainstorms.md`
- status: `absorbed`
- milestone: `M-20260306-workspace-routing-foundation`
- promoted_issue_path: `docs/B2-docs/ibm/global-ai-account-watchdog-and-manager-bootstrap/issues/global-ai-account-watchdog-and-manager-bootstrap.md`
- decision_reason: `I-20260318T163000Z` 已吸收 account active probe / cooldown recovery contract，当前候选只保留为该 canonical watchdog owner 的 supporting evidence，不再单独 materialize。
- session_refs:
  - tool: `codex`
    session_id: `current-thread`
    jsonl_path: `unavailable://codex-thread-only`
    role: `author`
- why_now:
  - 现有 cooldown 判断偏被动，恢复时间可能过时
  - 当前实现需要统一成显式代理下的 `codex exec "hi"` probe
  - 自动 probe 路径不能破坏既有切号/manager bootstrap 回归
- expected_outcome:
  - probe 返回可区分 `usable` 与 `rate_limited:<reset_at>`
  - cooldown 写回与自动切号共享同一套可验证语义
  - Freely 主管位在账号恢复前后能得到正确的切号与等待决策
- acceptance_hint:
  - `test-freely-ai-account-switch` 通过
  - `test-freely-rate-limit-defers-to-watchdog` 通过
  - `test-freely-ensure-manager` 通过
  - `governance-check` 通过
- next_action:
  - 已吸收到 `I-20260318T163000Z` 的 dev-loop / verification 生命周期
  - 下一步在当前 feature worktree 完成 checkpoint commit、promote 到 `develop`，再做 cleanup evidence
