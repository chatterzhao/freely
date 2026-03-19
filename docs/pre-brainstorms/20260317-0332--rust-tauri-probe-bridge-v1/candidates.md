# Candidates - 20260317-0332--rust-tauri-probe-bridge-v1

## Context
- Source brainstorm: `./brainstorms.md`
- Status: `active`

## Candidates

### C-20260317-0332
- title: `Rust/Tauri Probe Bridge v1`
- problem: `Frontend Probe v0` 的 frontend contract、transport diagnostics、manifest 与错误面已经基本收敛，但仓库里仍不存在任何 Rust/Tauri backend bridge 来提供 `probe_request_snapshot`、`probe_send_command`、`probe_server_event`。
- why_now: 如果 backend bridge 继续缺失，`I-20260317-1002` 只能反复在前端 mock seam 上空转，无法进入真实宿主与后端联调。
- acceptance_hint: 至少明确是否采用根目录 `src-tauri/ + Cargo.toml` 的 day-1 方案，冻结 `probe_request_snapshot` / `probe_send_command` / `probe_server_event` 的最小签名，并明确 day-1 最小 snapshot/event 子集。
- priority: `P0`
- status: `promoted`
- decision_reason: day-1 落点、三条 bridge、单 `probe_send_command` 入口和最小 snapshot/event 子集已经收敛到足够稳定，可直接提升为正式 backend issue。
- promoted_issue_path: `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/issues/rust-tauri-probe-bridge-v1.md`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- session_refs:
  - tool: `codex`
  - session_id: `current-thread`
  - jsonl_path: `unavailable://codex-thread-only`
  - role: `lead-agent-reroute`
