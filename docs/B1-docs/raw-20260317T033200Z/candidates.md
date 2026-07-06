# Candidates - 20260317-0332--rust-tauri-probe-bridge-v1

## Context
- Source brainstorm: `./brainstorms.md`
- Status: `completed`

## Candidates

### C-20260317T033200Z-A: legacy issue
- title: `Rust/Tauri Probe Bridge v1`
- problem: `Frontend Probe v0` 的 frontend contract、transport diagnostics、manifest 与错误面已经基本收敛，但仓库里仍不存在任何 Rust/Tauri backend bridge 来提供 `probe_request_snapshot`、`probe_send_command`、`probe_server_event`。
- why_now: 如果 backend bridge 继续缺失，`I-20260317T100200Z` 只能反复在前端 mock seam 上空转，无法进入真实宿主与后端联调。
- acceptance_hint: 至少明确是否采用根目录 `src-tauri/ + Cargo.toml` 的 day-1 方案，冻结 `probe_request_snapshot` / `probe_send_command` / `probe_server_event` 的最小签名，并明确 day-1 最小 snapshot/event 子集。
- priority: `P0`
- status: `completed`
- decision_reason: day-1 bridge 候选已经 materialize 为正式 owner，并由 `I-20260317T033200Z` 完成 canonical closeout。当前 candidate 仅保留为来源 provenance，不再代表活跃待办。
- promoted_issue_path: `docs/B2-docs/human/tui/raw-20260308-1244issues/rust-tauri-probe-bridge-v1.md`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- next_action: 保留为历史来源记录。若未来要扩展 beyond day-1 subset 的 bridge transport、事件面或宿主集成，应从当前 canonical truth 新开 candidate/issue，而不是恢复这条 candidate。
- completion_note: `I-20260317T033200Z` 已完成 canonical closeout；真实宿主启动验证与最小 `Transport=tauri` 闭环已吸收到 `develop`，因此该 candidate 不再构成活跃 queue。
- session_refs:
  - tool: `codex`
  - session_id: `current-thread`
  - jsonl_path: `unavailable://codex-thread-only`
  - role: `lead-agent-reroute`
