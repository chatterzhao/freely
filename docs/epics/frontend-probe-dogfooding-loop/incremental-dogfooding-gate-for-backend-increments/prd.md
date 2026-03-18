# PRD: incremental-dogfooding-gate-for-backend-increments

## Goal

把 Probe 验证从“推荐做法”提升为 Freely 自举开发的正式完成门禁。

## Requirements

1. 后端增量进入完成态前，必须具备 Probe 验证证据。
2. 证据必须至少覆盖：可触发、可观察、可中断、可回放。
3. 证据必须可回写到规范文档位置。
4. 当证据缺失时，必须阻断完成与提升。

## Product rules

1. 没有 Probe 验证证据的后端增量不算完成。
2. Freely 自举开发 Freely 时也必须满足同一门禁。
3. 门禁判定不能只依赖口头说明，必须依赖落盘证据。

## Minimal evidence fields

- `probe_entry`
- `probe_observation`
- `probe_interruptibility`
- `probe_replayability`
- `session_refs`
- `blocker` when incomplete
