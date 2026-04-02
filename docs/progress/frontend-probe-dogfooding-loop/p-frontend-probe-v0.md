# Progress: frontend-probe-v0

- issue_id: `I-20260308-1244-03`
- issue_path: `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
- title: `Frontend Probe v0`
- phase_state: `in_verification`
- milestone: `M-20260308-frontend-probe-dogfooding-loop`
- updated_at: `2026-04-02`
- summary:
  - frontend 侧 Probe shell、contract、transport、manifest 与错误面已经收敛到可持续推进的 day-1 产品面；embedded terminal 现在也具备真实 `AttachTerminal` 交互，而不再只是静态 target/stream 展示。
  - 真实 `bun run tauri:validate:probe` 已扩到 `start / session create-resume / terminal attach / chat intervention` 闭环，因此当前 owner 可从 `in_dev` 推进到 `in_verification`。
  - Recent Activity 现在会按宿主系统时区渲染事件时间并显示时区标签，显示层与底层 RFC3339 event truth 已解耦；更宽的 CLI/watchdog 时间边界仍留在 absorbed research，不在本轮前端 continuation 中扩张。
- evidence:
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/code-reviews/20260401-rust-tauri-probe-bridge-host-validation-verification.md`
  - `docs/epics/frontend-probe-dogfooding-loop/rust-tauri-probe-bridge-v1/code-reviews/20260401-rust-tauri-probe-bridge-real-interaction-verification.md`
  - `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/code-reviews/20260401-frontend-probe-v0-terminal-attach-validation.md`
- next:
  - 当前先把 implementation + verification evidence 合到 `develop`；之后再决定是否为 `frontend-probe-v0` 开纯治理 closeout
