# Pre-tests: rust-tauri-probe-bridge-v1

## Contract checks

1. 前端默认 bridge 名称与本 issue 定义一致：
   - `probe_request_snapshot`
   - `probe_send_command`
   - `probe_server_event`
2. 前端 `freely.probe.v1` manifest 与本 issue 的 day-1 contract 无冲突。

## Integration checks

1. backend 落地后，前端在 `tauri` 模式下不再显示 `bridge offline`。
2. `probe_request_snapshot` 至少返回单项目最小 snapshot。
3. `probe_send_command` 至少覆盖 control/session/chat 三类命令。
4. `probe_server_event` 至少回放 frontend 当前已消费的最小事件子集。
5. 前端 `Transport=tauri` 时，`Frontend Probe v0` 至少能完成一次 start、一次 session create/resume、一次 chat intervention 的最小联调。
