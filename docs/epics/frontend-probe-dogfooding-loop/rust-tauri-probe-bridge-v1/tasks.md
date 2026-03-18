# Tasks: rust-tauri-probe-bridge-v1

1. 建立根目录 `src-tauri/` 与 `Cargo.toml` 的最小 Tauri/Rust 基线。
2. 实现 `probe_request_snapshot` 的最小 day-1 返回面。
3. 实现单入口 `probe_send_command`，覆盖 control/session/chat 三类命令。
4. 实现 `probe_server_event` 的最小事件回放。
5. 用 `Frontend Probe v0` 做第一次真实宿主联调验证。
6. 把联调结果回写到 `I-20260317-1005` 与 `I-20260317-1002`，解除前端侧对 bridge 缺失的 blocker 描述。
