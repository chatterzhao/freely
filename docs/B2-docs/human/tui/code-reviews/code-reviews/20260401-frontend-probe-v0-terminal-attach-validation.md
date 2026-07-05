# Code Review: frontend-probe-v0-terminal-attach-validation

- issue_id: `I-20260308-1244-03`
- issue: `docs/epics/frontend-probe-dogfooding-loop/frontend-probe-v0/issues/frontend-probe-v0.md`
- reviewer: `codex`
- phase: `in_verification`
- date: `2026-04-01`

## Verdict

- pass_for_current_scope: `true`
- scope_note: `embedded terminal 已从只展示 target/stream 文本推进到真实 AttachTerminal 交互，并且真实 Tauri validation 已覆盖 start -> session -> attach -> chat 闭环`

## Evidence

1. `bun test src/frontend_probe_v0/adapter.test.ts src/frontend_probe_v0/tauriAdapter.test.ts`
   - result: passed
   - evidence:
     - `MockProbeAdapter` 会在 attach 后把 target 置顶、刷新 `governanceSummary`，并发出 `TerminalChunkAppended`
     - `TauriProbeAdapter` 仍保持正确的 snapshot invoke 形状与 eager event registration
2. `bun run typecheck`
   - result: passed
3. `bun run build`
   - result: passed
4. `cargo test -p freely-probe-bridge`
   - result: passed
   - evidence:
     - Rust bridge 已识别 `AttachTerminal`
     - attach payload 会更新 `terminal_targets/session` 与 `governance_summary`
5. `bun run tauri:validate:probe`
   - result: passed
   - evidence:
     - `observedCommands` 包含 `ControlRun`、`CreateOrResumeSession`、`AttachTerminal`、`SendChatIntervention`
     - `AttachTerminal` ack 为 `terminal attached: freely-run-1:pty-0`
     - attach 后 snapshot `governanceSummary` 包含 `terminal attached to freely-run-1:pty-0`
6. `bun test src/frontend_probe_v0/timeDisplay.test.ts`
   - result: passed
   - evidence:
     - RFC3339 event timestamps are rendered through host-system local timezone formatting with timezone label
     - unparseable values still pass through unchanged instead of displaying a fake local time

## Findings

- no_blocking_findings_for_current_scope: `true`
- residual_gap:
  - 当前证据证明 `Frontend Probe v0` 的最小 control/session/chat/terminal attach 流已可在真实 Tauri transport 下串起来；是否直接 canonical closeout 仍需后续纯治理判断，不在本轮实现 merge 内完成

## Writeback

- `I-20260308-1244-03` 已不再卡在 backend bridge blocker 或 embedded terminal attach 缺口，当前可从 `in_dev` 推进到 `in_verification`
- 当前轮不要把 owner 提前标成 `completed`；先让实现与验证证据进入 `develop`，再决定是否走纯治理 closeout

## Implementation Decision Note

- decision: `Keep frontend-probe-v0 time rendering narrowly at the display layer by formatting Recent Activity timestamps in the host system timezone, while leaving machine/store timestamps and backup/governance naming truth unchanged.`
- why_this: `The active user-facing gap is in Probe's Recent Activity readability. Formatting at the display edge fixes that without destabilizing RFC3339/epoch truth, backup naming order, or broader runtime governance semantics.`
- alternatives_considered: `Considered widening the same patch into ai-cli and watchdog human-readable fields or introducing a repo-wide time-governance owner first. That would mix frontend continuation with broader runtime surfaces before a shared contract and owner boundary are frozen.`
- boundary_non_goals: `This continuation does not rewrite backup naming to local time, does not change stored event/reset truth away from RFC3339 or epoch values, and does not claim repo-wide timezone unification across CLI, watchdog, and future TUI surfaces.`
- residual_risk: `frontend-probe-v0` still owns only the Probe display slice. Broader runtime/status timezone display alignment now routes through `I-20260402-0308-A`; future user-selectable timezone preferences or shared cross-shell formatter work should materialize there instead of widening this owner.`
