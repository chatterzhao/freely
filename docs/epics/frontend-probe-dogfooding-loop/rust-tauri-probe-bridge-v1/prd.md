# PRD: rust-tauri-probe-bridge-v1

## Goal

建立 `freely.probe.v1` 的最小 Rust/Tauri backend bridge，让 `Frontend Probe v0` 能在真实宿主上第一次接通。

## Requirements

1. 冻结根目录 `src-tauri/ + Cargo.toml` 的 day-1 落点。
2. 冻结三条 bridge 的最小签名。
3. 明确单 `probe_send_command` 入口的 command/payload 约束。
4. 明确 day-1 最小 snapshot/event 子集。
5. 明确 day-1 snapshot 至少返回 `projectId/projectName/governanceSummary/recoverySummary/lastEventId/activeRuns/activeAgents/sessions/terminalTargets`。
6. 明确 day-1 事件只要求覆盖 `RunStatusChanged/AgentStatusChanged/SessionUpserted/InputArbitrationRecorded/TerminalChunkAppended`。

## Product rules

1. 这是一条 backend bridge issue，不再伪装成 frontend seam 补丁。
2. day-1 优先追求真实宿主可接通，不优先追求后端抽象完美分层。
3. 事件与 snapshot 只覆盖 frontend 当前已消费的最小闭环。

## Exit criteria for `done_ibm`

1. 工程落点已冻结。
2. 三条 bridge 的最小 contract 已冻结。
3. day-1 snapshot/event 子集已冻结。
4. `Frontend Probe v0` 如何依赖这条 bridge 已明确。
